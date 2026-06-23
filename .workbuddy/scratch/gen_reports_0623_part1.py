#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate 4 World Cup prediction reports for June 24, 2026 — V5 (post-R1 data refresh)"""
import os

REPORTS_DIR = r"C:\Users\cocro\WorkBuddy\wc2026-reports\reports"
MD_DIR = r"D:\我的坚果云\OB笔记\自媒体\fwc2026\content\predictions"
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(MD_DIR, exist_ok=True)

NOW = "2026-06-23 17:25"
REPORT_DATE = "2026-06-24"

CSS = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; background: #fff; color: #111; line-height: 1.6; }
    .container { max-width: 960px; margin: 0 auto; padding: 40px 24px; }
    header { border-bottom: 2px solid #0033A0; padding-bottom: 24px; margin-bottom: 32px; }
    h1 { font-size: 2rem; font-weight: 800; color: #0033A0; }
    .meta { color: #555; font-size: 0.9rem; margin-top: 8px; }
    .meta span { margin-right: 16px; }
    .section { margin-bottom: 32px; padding: 24px; border: 1px solid #000; border-radius: 4px; }
    .section h2 { font-size: 1.2rem; font-weight: 700; color: #0033A0; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid #000; }
    .section h3 { font-size: 1rem; font-weight: 700; margin-bottom: 8px; }
    .dual-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    @media (max-width: 640px) { .dual-col { grid-template-columns: 1fr; } }
    .col p { margin-bottom: 8px; }
    table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 0.85rem; }
    th, td { border: 1px solid #000; padding: 6px 10px; text-align: left; }
    th { background: #0033A0; color: #fff; font-weight: 600; }
    .standings tr:nth-child(even) td { background: #f0f4ff; }
    .prob td { text-align: center; font-size: 1.3rem; font-weight: 700; }
    .prob td.win { background: #0033A0; color: #fff; }
    .score td { text-align: center; }
    .matchups th { background: #000; }
    .coach-view { margin-bottom: 16px; padding: 16px; border-left: 3px solid #0033A0; background: #f4f7fd; }
    .coach-view h3 { color: #0033A0; }
    .note { font-size: 0.85rem; color: #c0392b; background: #fef5f5; padding: 10px 14px; border-left: 3px solid #c0392b; margin: 12px 0; }
    .signal-strong { color: #c0392b; font-weight: 700; }
    .signal-mid { color: #e67e22; font-weight: 600; }
    .signal-weak { color: #7f8c8d; }
    .conclusion { background: #f0f4ff; border-color: #0033A0; }
    .conclusion h2 { color: #0033A0; }
    footer { margin-top: 48px; padding-top: 16px; border-top: 1px solid #000; font-size: 0.8rem; color: #888; text-align: center; }
    .players td:first-child { font-weight: 600; }
    .coach td:first-child { font-weight: 600; width: 120px; }
"""
