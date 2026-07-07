import streamlit as st

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2d6a4f 0%, #40916c 40%, #52b788 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.2rem;
    }

    .sub-header {
        font-size: 1rem;
        color: #6b7280;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }

    .kpi-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: transform 0.15s, box-shadow 0.15s;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #111827;
        line-height: 1.2;
    }
    .kpi-unit {
        font-size: 0.8rem;
        color: #9ca3af;
        font-weight: 400;
    }

    .metric-row {
        padding: 0.75rem 0;
        border-bottom: 1px solid #f3f4f6;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .metric-row:last-child { border-bottom: none; }
    .metric-name { font-weight: 500; color: #374151; }
    .metric-value { font-weight: 600; color: #111827; }

    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .status-REGENERATIVE { background: #d1fae5; color: #065f46; }
    .status-SUSTAINABLE { background: #dbeafe; color: #1e40af; }
    .status-STRAINED { background: #fef3c7; color: #92400e; }
    .status-MINING { background: #fee2e2; color: #991b1b; }
    .status-UNKNOWN { background: #f3f4f6; color: #6b7280; }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1f2937;
        margin: 1.5rem 0 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }

    .plant-tooltip {
        font-size: 0.85rem;
        color: #4b5563;
    }

    div[data-testid="stTabs"] button {
        font-weight: 500;
    }

    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
</style>
"""

HEALTH_COLORS = {
    "REGENERATIVE": "#059669",
    "SUSTAINABLE": "#2563eb",
    "STRAINED": "#d97706",
    "MINING": "#dc2626",
    "UNKNOWN": "#6b7280",
}

HEALTH_ICONS = {
    "REGENERATIVE": "🌿",
    "SUSTAINABLE": "🌱",
    "STRAINED": "⚠️",
    "MINING": "🔴",
    "UNKNOWN": "⚪",
}
