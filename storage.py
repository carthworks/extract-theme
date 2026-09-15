"""
storage.py — S3 / Cloudflare R2 Object Storage integration for ExtractTheme Studio.

Provides persistent storage for extracted design systems across Vercel / serverless deployments.
Supports:
  - Cloudflare R2 (S3 compatible)
  - AWS S3
  - Any S3-compatible object storage (MinIO, Wasabi, Backblaze B2)
"""

from __future__ import annotations

import io
import json
import mimetypes
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import boto3
    from botocore.client import Config
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False
    ClientError = Exception


# Common MIME types
MIME_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".md": "text/markdown; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".woff2": "font/woff2",
    ".woff": "font/woff",
    ".ttf": "font/ttf",
    ".eot": "application/vnd.ms-fontobject",
    ".otf": "font/otf",
}


def get_mime_type(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    return MIME_TYPES.get(ext, mimetypes.guess_type(filename)[0] or "application/octet-stream")


def _load_dotenv(path: Optional[Path] = None) -> None:
    """Zero-dependency .env file reader to populate os.environ if not already set."""
    env_path = path or (Path(__file__).parent / ".env")
    if not env_path.is_file():
        return
    try:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip("\"'")
            if key and key not in os.environ:
                os.environ[key] = val
    except Exception as exc:
        print(f"[Storage] Warning: Failed to parse .env file: {exc}")


class S3Storage:
    def __init__(self):
        _load_dotenv()
        self.bucket = os.environ.get("S3_BUCKET_NAME") or os.environ.get("AWS_S3_BUCKET_NAME") or ""
        self.endpoint_url = (
            os.environ.get("S3_ENDPOINT_URL")
            or os.environ.get("AWS_ENDPOINT_URL")
            or os.environ.get("R2_ENDPOINT_URL")
            or None
        )
        self.access_key = (
            os.environ.get("S3_ACCESS_KEY_ID")
            or os.environ.get("AWS_ACCESS_KEY_ID")
            or os.environ.get("R2_ACCESS_KEY_ID")
            or ""
        )
        self.secret_key = (
            os.environ.get("S3_SECRET_ACCESS_KEY")
            or os.environ.get("AWS_SECRET_ACCESS_KEY")
            or os.environ.get("R2_SECRET_ACCESS_KEY")
            or ""
        )
        self.region = (
            os.environ.get("S3_REGION_NAME")
            or os.environ.get("AWS_REGION")
            or os.environ.get("AWS_DEFAULT_REGION")
            or "auto"
        )
        self.prefix = os.environ.get("S3_KEY_PREFIX", "themes").strip("/")

        self._client = None
        if self.is_configured() and HAS_BOTO3:
            try:
                self._client = boto3.client(
                    "s3",
                    endpoint_url=self.endpoint_url,
                    aws_access_key_id=self.access_key,
                    aws_secret_access_key=self.secret_key,
                    region_name=self.region,
                    config=Config(signature_version="s3v4", s3={"addressing_style": "virtual" if not self.endpoint_url else "path"}),
                )
            except Exception as e:
                print(f"[Storage] Failed to initialize S3 client: {e}")
                self._client = None

    def is_configured(self) -> bool:
        return bool(self.bucket and self.access_key and self.secret_key and HAS_BOTO3)

    def upload_file(self, s3_key: str, data: bytes | str, content_type: Optional[str] = None) -> bool:
        if not self._client:
            return False
        try:
            if isinstance(data, str):
                body = data.encode("utf-8")
            else:
                body = data

            ct = content_type or get_mime_type(s3_key)
            self._client.put_object(
                Bucket=self.bucket,
                Key=s3_key,
                Body=body,
                ContentType=ct,
            )
            return True
        except Exception as exc:
            print(f"[Storage] Error uploading {s3_key}: {exc}")
            return False

    def upload_theme_directory(self, domain: str, local_dir: Path) -> int:
        """
        Uploads all generated files in local_dir to S3/R2 under {prefix}/{domain}/...
        Returns count of files successfully uploaded.
        """
        if not self._client or not local_dir.exists():
            return 0

        uploaded_count = 0
        try:
            for item in local_dir.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(local_dir).as_posix()
                    s3_key = f"{self.prefix}/{domain}/{rel_path}"
                    content_type = get_mime_type(item.name)
                    content = item.read_bytes()
                    if self.upload_file(s3_key, content, content_type):
                        uploaded_count += 1
            print(f"[Storage] Successfully synced {uploaded_count} files for {domain} to S3/R2.")
        except Exception as exc:
            print(f"[Storage] Error syncing theme directory {domain}: {exc}")

        return uploaded_count

    def get_file(self, rel_path: str) -> Optional[Tuple[bytes, str]]:
        """
        Fetches a file from S3 given a relative path like '{domain}/{filename}'.
        Returns (content_bytes, content_type) or None if not found.
        """
        if not self._client:
            return None

        clean_path = rel_path.strip("/")
        s3_key = f"{self.prefix}/{clean_path}"

        try:
            response = self._client.get_object(Bucket=self.bucket, Key=s3_key)
            content = response["Body"].read()
            content_type = response.get("ContentType") or get_mime_type(clean_path)
            return content, content_type
        except ClientError as e:
            if e.response.get("Error", {}).get("Code") in ("NoSuchKey", "404"):
                return None
            print(f"[Storage] S3 get_file error for {s3_key}: {e}")
            return None
        except Exception as exc:
            print(f"[Storage] S3 get_file error for {s3_key}: {exc}")
            return None

    def list_projects(self) -> List[Dict[str, Any]]:
        """
        Lists all project domains stored in S3/R2 and retrieves their metadata from design-tokens.json.
        """
        if not self._client:
            return []

        prefix = f"{self.prefix}/"
        projects_dict: Dict[str, Dict[str, Any]] = {}

        try:
            paginator = self._client.get_paginator("list_objects_v2")
            for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
                for obj in page.get("Contents", []):
                    key = obj.get("Key", "")
                    rel = key[len(prefix):]
                    parts = rel.split("/", 1)
                    if len(parts) < 2:
                        continue
                    domain, filename = parts[0], parts[1]

                    if domain not in projects_dict:
                        projects_dict[domain] = {
                            "domain": domain,
                            "path": f"s3://{self.bucket}/{self.prefix}/{domain}",
                            "files": [],
                            "has_style_guide": False,
                            "has_tokens": False,
                            "meta": {},
                        }

                    proj = projects_dict[domain]
                    if filename == "style-guide.html":
                        proj["has_style_guide"] = True
                    elif filename == "design-tokens.json":
                        proj["has_tokens"] = True

                    if "/" not in filename:
                        proj["files"].append(filename)
                    elif filename.startswith("fonts/"):
                        if "fonts/" not in proj["files"]:
                            proj["files"].append("fonts/")

            # Populate metadata by reading design-tokens.json for each domain
            for domain, proj in projects_dict.items():
                if proj["has_tokens"]:
                    try:
                        token_res = self.get_file(f"{domain}/design-tokens.json")
                        if token_res:
                            tokens = json.loads(token_res[0].decode("utf-8"))
                            colors_dict = tokens.get("colors", {}) if isinstance(tokens.get("colors"), dict) else {}
                            top_colors = list(colors_dict.values())[:10]
                            fonts_val = tokens.get("fonts", {})
                            fonts_count = len([k for k in fonts_val if isinstance(k, str) and not k.startswith("_")]) if isinstance(fonts_val, (dict, list)) else 0
                            fw = tokens.get("frameworks", {})
                            fw_list = list(fw.keys()) if isinstance(fw, dict) else (fw if isinstance(fw, list) else [])
                            proj["meta"] = {
                                "source": tokens.get("source") or "",
                                "generated": tokens.get("generated") or "",
                                "colors_count": len(colors_dict),
                                "top_colors": top_colors,
                                "roles": tokens.get("roles", {}) if isinstance(tokens.get("roles"), dict) else {},
                                "fonts_count": fonts_count,
                                "font_files_count": len(tokens.get("font_files", [])) if isinstance(tokens.get("font_files"), list) else 0,
                                "gradients_count": len(tokens.get("gradients", [])) if isinstance(tokens.get("gradients"), list) else 0,
                                "frameworks": fw_list,
                                "logo": tokens.get("logo"),
                            }
                    except Exception as exc:
                        print(f"[Storage] Error reading tokens for remote project {domain}: {exc}")

            projects_list = list(projects_dict.values())
            projects_list.sort(key=lambda p: str(p.get("meta", {}).get("generated") or ""), reverse=True)
            return projects_list
        except Exception as exc:
            print(f"[Storage] Error listing S3 projects: {exc}")
            return []


# Global singleton
storage = S3Storage()
