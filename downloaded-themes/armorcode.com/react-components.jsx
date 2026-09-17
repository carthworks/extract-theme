// Generated React Components for armorcode.com
// Built with tokens extracted by ExtractTheme Studio

import React from 'react';

export function Button({ children, variant = 'primary', className = '', ...props }) {
  const baseStyle = {
    padding: '10px 20px',
    borderRadius: '8px',
    fontWeight: 600,
    fontSize: '14px',
    cursor: 'pointer',
    border: 'none',
    transition: 'all 0.15s ease-in-out',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
  };

  const variants = {
    primary: {
      backgroundColor: 'var(--color-primary, #f3f3ff)',
      color: '#ffffff',
    },
    secondary: {
      backgroundColor: 'transparent',
      border: '1px solid rgba(128, 128, 128, 0.3)',
      color: 'inherit',
    },
  };

  return (
    <button style={{ ...baseStyle, ...variants[variant] }} className={className} {...props}>
      {children}
    </button>
  );
}

export function Card({ title, subtitle, children, className = '' }) {
  return (
    <div
      style={{
        padding: '24px',
        borderRadius: '12px',
        border: '1px solid rgba(128, 128, 128, 0.2)',
        backgroundColor: 'var(--color-surface, rgba(255, 255, 255, 0.03))',
        boxShadow: '0 4px 16px rgba(0, 0, 0, 0.08)',
      }}
      className={className}
    >
      {title && <h3 style={{ margin: '0 0 8px 0', fontSize: '18px', fontWeight: 600 }}>{title}</h3>}
      {subtitle && <p style={{ margin: '0 0 16px 0', opacity: 0.7, fontSize: '14px' }}>{subtitle}</p>}
      {children}
    </div>
  );
}

export function Hero({ headline, description, ctaText = 'Get Started', onCtaClick }) {
  return (
    <section style={{ padding: '64px 24px', textAlign: 'center', maxWidth: '960px', margin: '0 auto' }}>
      <h1 style={{ fontSize: '42px', fontWeight: 700, letterSpacing: '-0.02em', marginBottom: '16px' }}>
        {headline}
      </h1>
      <p style={{ fontSize: '18px', opacity: 0.8, maxWidth: '640px', margin: '0 auto 28px' }}>
        {description}
      </p>
      <Button variant="primary" onClick={onCtaClick}>{ctaText}</Button>
    </section>
  );
}
