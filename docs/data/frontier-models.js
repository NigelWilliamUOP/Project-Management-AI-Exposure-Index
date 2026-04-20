window.PM_FRONTIER_MODEL_DATA = {
  "generated_at_utc": "2026-04-20T19:21:24.041199+00:00",
  "snapshot_month": "2026-04",
  "repo_name": "Project-Management-AI-Exposure-Index",
  "view_type": "frontier_model_families",
  "methodology": {
    "aggregation_rule": "For each frontier model family and benchmark, keep the highest-scoring matched public system entry in the current snapshot, then recompute the PM exposure scores from those family-level benchmark rows.",
    "caution": "This is a best-observed public-system view of underlying model families, not a scaffold-neutral laboratory comparison."
  },
  "occupation": {
    "occupation_code": "15-1299.09",
    "occupation_label": "Project Management Specialists / Information Project Managers",
    "weighted_dae_100": 68.09,
    "weighted_se_100": 20.03,
    "weighted_oc_100": 72.38,
    "weighted_ic_100": 28.37,
    "included_task_count": 21
  },
  "summary": {
    "tracked_model_count": 38,
    "matched_source_system_count": 118,
    "selected_benchmark_row_count": 38,
    "provider_count": 9,
    "top_model": {
      "frontier_model_id": "openai_gpt_5_4",
      "display_name": "GPT-5.4",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 25.0371
    },
    "median_realized_occupation_exposure_100": 13.1307,
    "mean_benchmark_coverage_ratio": 0.0543
  },
  "rows": [
    {
      "frontier_model_id": "openai_gpt_5_4",
      "display_name": "GPT-5.4",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 25.0371,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: ForgeCode | GPT-5.4"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 1
    },
    {
      "frontier_model_id": "google_gemini_3_1_pro",
      "display_name": "Gemini 3.1 Pro",
      "provider": "Google",
      "realized_occupation_exposure_100": 24.5474,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: TongAgents | Gemini 3.1 Pro"
      ],
      "source_system_count": 3,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 2
    },
    {
      "frontier_model_id": "anthropic_claude_opus_4_6",
      "display_name": "Claude Opus 4.6",
      "provider": "Anthropic",
      "realized_occupation_exposure_100": 24.425,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: ForgeCode | Claude Opus 4.6"
      ],
      "source_system_count": 10,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 3
    },
    {
      "frontier_model_id": "openai_gpt_5_3_codex",
      "display_name": "GPT-5.3-Codex",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 23.9964,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: SageAgent | GPT-5.3-Codex"
      ],
      "source_system_count": 7,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 4
    },
    {
      "frontier_model_id": "google_gemini_3_pro",
      "display_name": "Gemini 3 Pro",
      "provider": "Google",
      "realized_occupation_exposure_100": 21.2418,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Ante | Gemini 3 Pro"
      ],
      "source_system_count": 7,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 5
    },
    {
      "frontier_model_id": "openai_gpt_5_2_codex",
      "display_name": "GPT-5.2-Codex",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 20.3541,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Deep Agents | GPT-5.2-Codex"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 6
    },
    {
      "frontier_model_id": "openai_gpt_5_2",
      "display_name": "GPT-5.2",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 19.8644,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Droid | GPT-5.2"
      ],
      "source_system_count": 4,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 7
    },
    {
      "frontier_model_id": "google_gemini_3_flash",
      "display_name": "Gemini 3 Flash",
      "provider": "Google",
      "realized_occupation_exposure_100": 19.6808,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Junie CLI | Gemini 3 Flash"
      ],
      "source_system_count": 3,
      "selected_system_count": 1,
      "notes": "Fast frontier family derived from benchmark-specific public system entries.",
      "rank": 8
    },
    {
      "frontier_model_id": "anthropic_claude_opus_4_5",
      "display_name": "Claude Opus 4.5",
      "provider": "Anthropic",
      "realized_occupation_exposure_100": 19.3135,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Droid | Claude Opus 4.5"
      ],
      "source_system_count": 8,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 9
    },
    {
      "frontier_model_id": "openai_gpt_5_1_codex_max",
      "display_name": "GPT-5.1-Codex-Max",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 18.4871,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Codex CLI | GPT-5.1-Codex-Max"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 10
    },
    {
      "frontier_model_id": "openai_gpt_5_1_codex",
      "display_name": "GPT-5.1-Codex",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 17.6913,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Crux | GPT-5.1-Codex"
      ],
      "source_system_count": 3,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 11
    },
    {
      "frontier_model_id": "xai_grok_4_20_reasoning",
      "display_name": "Grok 4.20 Reasoning",
      "provider": "xAI",
      "realized_occupation_exposure_100": 17.5382,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: grok-cli | Grok 4.20 Reasoning"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 12
    },
    {
      "frontier_model_id": "zhipu_glm_5",
      "display_name": "GLM 5",
      "provider": "Zhipu",
      "realized_occupation_exposure_100": 16.0384,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | GLM 5"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family represented in the public benchmark snapshot.",
      "rank": 13
    },
    {
      "frontier_model_id": "openai_gpt_5",
      "display_name": "GPT-5",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 15.1814,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Codex CLI | GPT-5"
      ],
      "source_system_count": 4,
      "selected_system_count": 1,
      "notes": "Catch-all GPT-5 family for rows that are not labeled with a more specific GPT-5 variant.",
      "rank": 14
    },
    {
      "frontier_model_id": "openai_gpt_5_1",
      "display_name": "GPT-5.1",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 14.5693,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | GPT-5.1"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 15
    },
    {
      "frontier_model_id": "anthropic_claude_sonnet_4_5",
      "display_name": "Claude Sonnet 4.5",
      "provider": "Anthropic",
      "realized_occupation_exposure_100": 14.2326,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: CAMEL-AI | Claude Sonnet 4.5"
      ],
      "source_system_count": 7,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 16
    },
    {
      "frontier_model_id": "openai_gpt_5_codex",
      "display_name": "GPT-5-Codex",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 13.5592,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Codex CLI | GPT-5-Codex"
      ],
      "source_system_count": 3,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 17
    },
    {
      "frontier_model_id": "moonshot_kimi_k2_5",
      "display_name": "Kimi K2.5",
      "provider": "Moonshot AI",
      "realized_occupation_exposure_100": 13.2225,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | Kimi K2.5"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family represented in the public benchmark snapshot.",
      "rank": 18
    },
    {
      "frontier_model_id": "openai_gpt_5_1_codex_mini",
      "display_name": "GPT-5.1-Codex-Mini",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 13.1919,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Crux | GPT-5.1-Codex-Mini"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 19
    },
    {
      "frontier_model_id": "minimax_m2_5",
      "display_name": "MiniMax M2.5",
      "provider": "MiniMax",
      "realized_occupation_exposure_100": 13.0695,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: cchuter | minimax-m2.5"
      ],
      "source_system_count": 2,
      "selected_system_count": 1,
      "notes": "Frontier family represented in the public benchmark snapshot.",
      "rank": 20
    },
    {
      "frontier_model_id": "deepseek_v3_2",
      "display_name": "DeepSeek-V3.2",
      "provider": "DeepSeek",
      "realized_occupation_exposure_100": 12.1207,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | DeepSeek-V3.2"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family represented in the public benchmark snapshot.",
      "rank": 21
    },
    {
      "frontier_model_id": "anthropic_claude_opus_4_1",
      "display_name": "Claude Opus 4.1",
      "provider": "Anthropic",
      "realized_occupation_exposure_100": 11.6309,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | Claude Opus 4.1"
      ],
      "source_system_count": 4,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 22
    },
    {
      "frontier_model_id": "minimax_m2_1",
      "display_name": "MiniMax M2.1",
      "provider": "MiniMax",
      "realized_occupation_exposure_100": 11.2024,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Crux | MiniMax M2.1"
      ],
      "source_system_count": 2,
      "selected_system_count": 1,
      "notes": "Frontier family represented in the public benchmark snapshot.",
      "rank": 23
    },
    {
      "frontier_model_id": "moonshot_kimi_k2_thinking",
      "display_name": "Kimi K2 Thinking",
      "provider": "Moonshot AI",
      "realized_occupation_exposure_100": 10.927,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | Kimi K2 Thinking"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Reasoning family represented in the public benchmark snapshot.",
      "rank": 24
    },
    {
      "frontier_model_id": "anthropic_claude_haiku_4_5",
      "display_name": "Claude Haiku 4.5",
      "provider": "Anthropic",
      "realized_occupation_exposure_100": 10.8657,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Goose | Claude Haiku 4.5"
      ],
      "source_system_count": 5,
      "selected_system_count": 1,
      "notes": "Fast frontier family derived from benchmark-specific public system entries.",
      "rank": 25
    },
    {
      "frontier_model_id": "openai_gpt_5_mini",
      "display_name": "GPT-5-Mini",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 10.6515,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: spoox-m | GPT-5-Mini"
      ],
      "source_system_count": 5,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 26
    },
    {
      "frontier_model_id": "zhipu_glm_4_7",
      "display_name": "GLM 4.7",
      "provider": "Zhipu",
      "realized_occupation_exposure_100": 10.223,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | GLM 4.7"
      ],
      "source_system_count": 2,
      "selected_system_count": 1,
      "notes": "Frontier family represented in the public benchmark snapshot.",
      "rank": 27
    },
    {
      "frontier_model_id": "google_gemini_2_5_pro",
      "display_name": "Gemini 2.5 Pro",
      "provider": "Google",
      "realized_occupation_exposure_100": 9.9781,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | Gemini 2.5 Pro"
      ],
      "source_system_count": 4,
      "selected_system_count": 1,
      "notes": "Near-frontier family represented in the public benchmark snapshot.",
      "rank": 28
    },
    {
      "frontier_model_id": "minimax_m2",
      "display_name": "MiniMax M2",
      "provider": "MiniMax",
      "realized_occupation_exposure_100": 9.1823,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | MiniMax M2"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Frontier family represented in the public benchmark snapshot.",
      "rank": 29
    },
    {
      "frontier_model_id": "moonshot_kimi_k2_instruct",
      "display_name": "Kimi K2 Instruct",
      "provider": "Moonshot AI",
      "realized_occupation_exposure_100": 8.5089,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | Kimi K2 Instruct"
      ],
      "source_system_count": 2,
      "selected_system_count": 1,
      "notes": "Instruction-tuned family represented in the public benchmark snapshot.",
      "rank": 30
    },
    {
      "frontier_model_id": "xai_grok_4",
      "display_name": "Grok 4",
      "provider": "xAI",
      "realized_occupation_exposure_100": 8.3253,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: OpenHands | Grok 4"
      ],
      "source_system_count": 3,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 31
    },
    {
      "frontier_model_id": "alibaba_qwen_3_coder_480b",
      "display_name": "Qwen 3 Coder 480B",
      "provider": "Alibaba",
      "realized_occupation_exposure_100": 8.3253,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Dakou Agent | Qwen 3 Coder 480B"
      ],
      "source_system_count": 3,
      "selected_system_count": 1,
      "notes": "Large coding family represented in the public benchmark snapshot.",
      "rank": 32
    },
    {
      "frontier_model_id": "xai_grok_code_fast_1",
      "display_name": "Grok Code Fast 1",
      "provider": "xAI",
      "realized_occupation_exposure_100": 7.8968,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Mini-SWE-Agent | Grok Code Fast 1"
      ],
      "source_system_count": 2,
      "selected_system_count": 1,
      "notes": "Specialized coding family represented in the public benchmark snapshot.",
      "rank": 33
    },
    {
      "frontier_model_id": "zhipu_glm_4_6",
      "display_name": "GLM 4.6",
      "provider": "Zhipu",
      "realized_occupation_exposure_100": 7.4989,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | GLM 4.6"
      ],
      "source_system_count": 1,
      "selected_system_count": 1,
      "notes": "Near-frontier family represented in the public benchmark snapshot.",
      "rank": 34
    },
    {
      "frontier_model_id": "openai_gpt_oss_120b",
      "display_name": "GPT-OSS-120B",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 5.7237,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | GPT-OSS-120B"
      ],
      "source_system_count": 2,
      "selected_system_count": 1,
      "notes": "Open-weight family represented in the public benchmark snapshot.",
      "rank": 35
    },
    {
      "frontier_model_id": "google_gemini_2_5_flash",
      "display_name": "Gemini 2.5 Flash",
      "provider": "Google",
      "realized_occupation_exposure_100": 5.2339,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Mini-SWE-Agent | Gemini 2.5 Flash"
      ],
      "source_system_count": 4,
      "selected_system_count": 1,
      "notes": "Near-frontier family represented in the public benchmark snapshot.",
      "rank": 36
    },
    {
      "frontier_model_id": "openai_gpt_oss_20b",
      "display_name": "GPT-OSS-20B",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 5.2033,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Terminus 2 | AfterQuery-GPT-OSS-20B"
      ],
      "source_system_count": 3,
      "selected_system_count": 1,
      "notes": "Open-weight family represented in the public benchmark snapshot.",
      "rank": 37
    },
    {
      "frontier_model_id": "openai_gpt_5_nano",
      "display_name": "GPT-5-Nano",
      "provider": "OpenAI",
      "realized_occupation_exposure_100": 3.5199,
      "benchmark_coverage_ratio": 0.0543,
      "benchmark_count": 1,
      "benchmarks": [
        "terminal_bench_2"
      ],
      "selected_systems": [
        "terminal_bench_2: Codex CLI | GPT-5-Nano"
      ],
      "source_system_count": 4,
      "selected_system_count": 1,
      "notes": "Frontier family derived from benchmark-specific public system entries.",
      "rank": 38
    }
  ]
};
