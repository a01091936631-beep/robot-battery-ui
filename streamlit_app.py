import base64
import json
import mimetypes
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LG ROBO CARE | 홈지니 키우기",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      [data-testid="stDecoration"],
      [data-testid="stSidebar"] {display:none!important;}
      #MainMenu, footer {visibility:hidden!important;}
      .stApp{
        background:
          radial-gradient(circle at 18% 10%,#fff9ec 0,transparent 30%),
          radial-gradient(circle at 88% 88%,#ead2a8 0,transparent 28%),
          #eee5d8;
      }
      .block-container{max-width:100%;padding:8px 4px 18px;}
      iframe{border:0!important;border-radius:28px;}
    

/* ===== Home UX restructure: map-only + AI 맞춤청소 / 직접조건청소 ===== */
.map-section .home-map-card.map-only-card{
  margin:0!important;
  padding:0!important;
  border:0!important;
  background:transparent!important;
  box-shadow:none!important;
}
.map-section .home-map-card.map-only-card .home-map-img-wrap{
  margin:0!important;
}
.ai-clean-controls{
  display:none;
}
.ai-clean-intro{
  display:flex;
  align-items:flex-start;
  gap:10px;
  padding:12px 12px;
  margin-bottom:10px;
  border-radius:14px;
  background:linear-gradient(145deg,#f1fae8,#fff6da);
  border:1px solid rgba(73,163,68,.18);
}
.ai-clean-intro-icon{
  flex:0 0 auto;
  width:38px;
  height:38px;
  display:grid;
  place-items:center;
  border-radius:12px;
  background:#e3f4d6;
  font-size:21px;
}
.ai-clean-intro-title{
  color:#2f7f37;
  font-size:13.5px;
  line-height:1.35;
  font-weight:800;
}
.ai-clean-intro-desc{
  margin-top:4px;
  color:#6e523a;
  font-size:11.5px;
  line-height:1.52;
  font-weight:500;
}
.ai-clean-mode-row{
  display:grid;
  grid-template-columns:1fr 1fr 1fr;
  gap:7px;
}
.ai-clean-mode-btn{
  min-height:45px;
  padding:7px 4px;
  border:1px solid rgba(124,83,43,.16);
  border-radius:13px;
  background:#fff4d8;
  color:#61452f;
  font-size:11.5px;
  line-height:1.25;
  font-weight:700;
  box-shadow:0 3px 7px rgba(79,48,21,.07);
}
.ai-clean-mode-btn.active{
  border-color:transparent;
  color:#fff;
  background:linear-gradient(135deg,#4ba746,#77c75b);
  box-shadow:0 6px 12px rgba(67,126,56,.20);
}
.ai-clean-mode-btn.danger.active{
  background:linear-gradient(135deg,#f07a54,#f7a13e);
  box-shadow:0 6px 12px rgba(190,93,45,.18);
}
.ai-clean-mode-btn:disabled{opacity:.55;cursor:not-allowed;}
.ai-clean-selection-note{
  margin-top:8px;
  padding:9px 10px;
  border-radius:12px;
  background:rgba(255,250,235,.94);
  border:1px solid rgba(124,83,43,.11);
  color:#6c4e36;
  font-size:11px;
  line-height:1.45;
  font-weight:500;
  text-align:center;
}
.ai-clean-selection-note b{color:#2f8b3a;font-weight:800;}
.ai-clean-now-btn{
  position:relative;
  z-index:35;
  width:100%;
  min-height:50px;
  margin-top:9px;
  padding:9px 12px;
  border:0;
  border-radius:14px;
  background:linear-gradient(90deg,#ef8c32,#ffad45);
  color:#fff;
  font-size:14px;
  line-height:1.2;
  font-weight:800;
  box-shadow:0 7px 14px rgba(210,117,35,.22);
}
.ai-clean-now-btn span{
  display:block;
  margin-top:3px;
  color:rgba(255,255,255,.88);
  font-size:10.5px;
  font-weight:500;
}
.ai-clean-now-btn:disabled{opacity:.58;filter:grayscale(.08);box-shadow:none;}
.prep-section.ai-ready .learn-panel{display:none!important;}
.prep-section.ai-ready .ai-clean-controls{display:block!important;}
.prep-section.ai-ready .plan-model{background:#e7f4d9;color:#2f8b3a;}
.direct-clean-section{
  border-top:3px solid rgba(239,140,50,.55)!important;
}
.prep-section{
  border-top:3px solid rgba(75,167,70,.48)!important;
}
@media(max-width:360px){
  .ai-clean-mode-btn{font-size:10.7px;min-height:44px;padding:6px 2px;}
  .ai-clean-intro-desc{font-size:11px;}
}

/* ===== Home visual adjustment: bigger station + mission moved right ===== */
#homePage .house{
  left:76px!important;
  top:112px!important;
  width:94px!important;
  height:80px!important;
  border-radius:38px 38px 9px 9px!important;
  box-shadow:0 8px 14px rgba(54,36,23,.24)!important;
}
#homePage .house:before{
  left:27px!important;
  bottom:0!important;
  width:40px!important;
  height:44px!important;
  border-radius:20px 20px 0 0!important;
}
#homePage .house:after{
  top:13px!important;
  left:27px!important;
  font-size:8.5px!important;
  letter-spacing:.2px!important;
}
#homePage .mission{
  left:auto!important;
  right:10px!important;
  bottom:14px!important;
  width:96px!important;
  z-index:18!important;
}


/* ===== Reward page simplification: level card removed, items shown immediately ===== */
#rewardPage .reward-folder-tabs{margin-top:2px!important;}
#rewardPage .section-title{margin-bottom:8px!important;}
</style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# 맞춤 배터리 준비 결과 기록 연결부
# GitHub에는 아래 구조로 기록을 올리면 됩니다.
# data/home_model_predictions.csv
# data/zone_model_predictions.csv
#
# 사진첩 / 분실물 이미지 연결부 (시연용)
# assets/photos/        → 4번째 탭 "사진첩"에 표시되는 반려동물 사진 (png/jpg/jpeg/gif/webp)
# assets/lost_items/    → 4번째 탭 "오늘의 발견"의 분실물 사진 (없으면 이모지로 표시)
# 각 폴더에 선택적으로 captions.json 을 두면 파일명별 제목/장소/시간/설명을 지정할 수 있습니다.
#   { "dog3_jpg": {"title": "안방에서 쉬는 중", "place": "안방", "time": "오늘 오후", "note": "홈지니가 살포시 담은 사진"} }
# captions.json 이 없으면 파일명(확장자 제외)이 제목으로 사용됩니다.
# 사진은 한 장당 1MB 이하로 줄여두면 로딩이 빠릅니다.
# ============================================================


BASE_DIR = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
DATA_DIR = BASE_DIR / "data"

# ============================================================
# 최종 ML 결과파일 연결부
# ============================================================
# 새 구조:
# data/ml_output.csv
#
# 머신러닝팀 최종 파일은 1행 = 1개 zone 청소 예측 결과입니다.
# 소형/중형/대형은 각각 4/6/8개 zone으로 구성됩니다.
#
# 집 전체 필요 SOC는 zone별 필요 SOC(zone_soc_used_pct)를 합산해서 계산합니다.
# 주의: zone_target_soc_pct를 합산하지 않습니다.
# zone_target_soc_pct는 zone 1개를 단독 청소할 때의 안전마진 포함 목표치입니다.
#
# fallback:
# 예전 파일명으로 업로드해도 동작하도록 ml_output(2).csv도 같이 탐색합니다.
# 예전 home_model_predictions.csv / zone_model_predictions.csv도 fallback으로 유지합니다.
# ============================================================

ML_OUTPUT_PATH = DATA_DIR / "ml_output.csv"
ML_OUTPUT_ALT_PATH = DATA_DIR / "ml_output(2).csv"
HOME_PRED_PATH = DATA_DIR / "home_model_predictions.csv"
ZONE_PRED_PATH = DATA_DIR / "zone_model_predictions.csv"

ASSET_DIR = BASE_DIR / "assets"
PHOTO_DIR = ASSET_DIR / "photos"
LOST_DIR = ASSET_DIR / "lost_items"

# 데모용 현재 배터리. 실제 제품에서는 로봇/앱에서 받은 현재 배터리로 교체하면 됩니다.
CURRENT_SOC = 80

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
IMAGE_NAME_ALLOWLIST = {"dog3_jpg"}


def _folder_signature(folder: Path):
    """폴더 안 파일이 바뀌면 캐시가 자동으로 갱신되도록 시그니처를 만듭니다."""
    if not folder.exists():
        return "missing"
    parts = []
    for p in sorted(folder.iterdir()):
        try:
            parts.append(f"{p.name}:{p.stat().st_mtime_ns}:{p.stat().st_size}")
        except Exception:
            parts.append(p.name)
    return "|".join(parts)


@st.cache_data
def load_image_folder(folder_str: str, signature: str):
    folder = Path(folder_str)
    items = []
    if not folder.exists() or not folder.is_dir():
        return items
    captions = {}
    cap_path = folder / "captions.json"
    if cap_path.exists():
        try:
            captions = json.loads(cap_path.read_text(encoding="utf-8")) or {}
        except Exception:
            captions = {}
    for p in sorted(folder.iterdir()):
        if p.suffix.lower() not in IMAGE_EXTS and p.name.lower() not in IMAGE_NAME_ALLOWLIST:
            continue
        try:
            raw = p.read_bytes()
        except Exception:
            continue
        mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
        data = base64.b64encode(raw).decode("ascii")
        default_photo_meta = {
            "dog1.jpg": {
                "title": "홈지니가 신기한 강아지",
                "place": "안방",
                "time": "오늘 오전 11:05",
                "note": "안방에서 강아지가 홈지니에게 관심을 보여서 살포시 찍어봤어요.",
            },
            "dog1_jpg": {
                "title": "홈지니가 신기한 강아지",
                "place": "안방",
                "time": "오늘 오전 11:05",
                "note": "안방에서 강아지가 홈지니에게 관심을 보여서 살포시 찍어봤어요.",
            },
            "dog1_jpg.jpg": {
                "title": "홈지니가 신기한 강아지",
                "place": "안방",
                "time": "오늘 오전 11:05",
                "note": "안방에서 강아지가 홈지니에게 관심을 보여서 살포시 찍어봤어요.",
            },
            "dog2.jpg": {
                "title": "강아지의 하루 기록",
                "place": "침실",
                "time": "오늘 오전",
                "note": "홈지니가 청소하면서 반려동물의 모습을 사진첩에 남겼어요.",
            },
            "dog3.jpg": {
                "title": "안방에서 쉬는 중",
                "place": "안방",
                "time": "오늘 오후",
                "note": "안방에서 편안히 쉬고 있는 모습을 홈지니가 살포시 담았어요.",
            },
            "dog3_jpg.jpg": {
                "title": "안방에서 쉬는 중",
                "place": "안방",
                "time": "오늘 오후",
                "note": "안방에서 편안히 쉬고 있는 모습을 홈지니가 살포시 담았어요.",
            },
            "dog3_jpg": {
                "title": "안방에서 쉬는 중",
                "place": "안방",
                "time": "오늘 오후",
                "note": "안방에서 편안히 쉬고 있는 모습을 홈지니가 살포시 담았어요.",
            },
        }
        default_meta = default_photo_meta.get(p.name.lower()) or default_photo_meta.get(p.stem.lower()) or {}
        # dog1/dog2/dog3는 시연 문구가 고정되어야 해서 기본 문구를 우선 적용합니다.
        if p.name.lower() in default_photo_meta or p.stem.lower() in default_photo_meta:
            meta = default_meta
        else:
            meta = captions.get(p.name) or captions.get(p.stem) or default_meta or {}
        if not isinstance(meta, dict):
            meta = {"title": str(meta)}
        items.append({
            "name": p.name,
            "src": f"data:{mime};base64,{data}",
            "title": str(meta.get("title") or p.stem),
            "place": str(meta.get("place") or ""),
            "time": str(meta.get("time") or ""),
            "note": str(meta.get("note") or ""),
        })
    return items


def _is_valid(value):
    return value is not None and not pd.isna(value)


def _safe_text(row, candidates, default=""):
    if row is None:
        return default
    for col in candidates:
        if col in row.index and _is_valid(row[col]):
            return str(row[col])
    return default


def _safe_float(row, candidates, default=0.0):
    if row is None:
        return float(default)
    for col in candidates:
        if col in row.index and _is_valid(row[col]):
            try:
                return float(row[col])
            except Exception:
                pass
    return float(default)


def _safe_int(row, candidates, default=0):
    try:
        return int(round(_safe_float(row, candidates, default)))
    except Exception:
        return int(default)


def _soc_target(required_soc):
    return int(round(max(15, min(float(required_soc) + 15, 90))))


def _infer_mop(row, prefix=""):
    """cleaning_type 또는 cleaning_type_code 기반으로 물걸레 여부를 추정합니다."""
    text_candidates = [
        f"{prefix}cleaning_type" if prefix else "cleaning_type",
        "cleaning_type_first",
        "cleaning_type",
    ]
    code_candidates = [
        f"{prefix}cleaning_type_code" if prefix else "cleaning_type_code",
        "cleaning_type_code_first",
        "cleaning_type_code",
    ]

    txt = _safe_text(row, text_candidates, "").lower()
    if any(k in txt for k in ["물", "걸레", "mop", "wet"]):
        return True
    if any(k in txt for k in ["건식", "dry"]):
        return False

    code = _safe_float(row, code_candidates, 0)
    return int(round(code)) == 1


@st.cache_data
def load_prediction_csv(path: str):
    p = Path(path)
    if not p.exists():
        return None
    df = pd.read_csv(p)
    if "global_run_id" in df.columns:
        df["global_run_id"] = df["global_run_id"].astype(str)
    return df


def _first_existing_csv(paths):
    for p in paths:
        if p.exists():
            return p
    return None


def _make_demo_runs():
    runs = []
    demo_specs = [
        (18, 4), (24, 4),
        (28, 6), (34, 6), (42, 6),
        (54, 8), (63, 8), (72, 8),
    ]

    for area, zone_count in demo_specs:
        for mop_enabled in [False, True]:
            base = area * 0.72 + (7 if mop_enabled else 0)
            labels_by_count = {
                4: ["거실", "주방", "침실", "현관"],
                6: ["침실", "주방", "거실", "서재", "현관", "다용도"],
                8: ["침실1", "침실2", "주방", "거실", "아이방", "현관", "서재", "다용도"],
            }
            floors = ["마루/타일", "장판/PVC", "저파일 러그", "고파일 카펫", "마루/타일", "장판/PVC", "저파일 러그", "마루/타일"]
            dirts = ["낮음", "보통", "높음", "낮음", "보통", "높음", "낮음", "보통"]
            weights = {
                4: [0.30, 0.24, 0.28, 0.18],
                6: [0.17, 0.19, 0.25, 0.15, 0.12, 0.12],
                8: [0.12, 0.11, 0.14, 0.20, 0.10, 0.12, 0.11, 0.10],
            }[zone_count]

            zones = []
            for i, w in enumerate(weights, start=1):
                required = max(1.2, base * w)
                dirt = dirts[i - 1]
                zones.append({
                    "scope": "zone",
                    "zone": i,
                    "label": f"{i}구역",
                    "globalRunId": f"demo_{area}_{'mop' if mop_enabled else 'dry'}",
                    "areaPyung": area,
                    "zoneCount": zone_count,
                    "cleaningAreaM2": round(area * 3.3058 * 0.82 * w, 1),
                    "requiredSoc": round(required, 1),
                    "targetSoc": _soc_target(required),
                    "modelName": "Final ML",
                    "cleaningType": "물걸레" if mop_enabled else "건식",
                    "cleaningTypeCode": 1 if mop_enabled else 0,
                    "mopEnabled": mop_enabled,
                    "obstacleLevel": "보통",
                    "obstacleLevelCode": 2,
                    "floorType": floors[i - 1],
                    "dirtLevel": dirt,
                    "dirtCode": 3 if dirt == "높음" else (2 if dirt == "보통" else 1),
                    "suctionMode": "자동",
                    "suctionCode": 2,
                    "needsRecharge": "무충전 완주 가능",
                    "chargeCount": 0,
                })

            home_required = round(sum(z["requiredSoc"] for z in zones), 1)
            home = {
                "scope": "home",
                "label": "집 전체",
                "globalRunId": f"demo_{area}_{'mop' if mop_enabled else 'dry'}",
                "areaPyung": area,
                "zoneCount": zone_count,
                "cleaningAreaM2": round(sum(z["cleaningAreaM2"] for z in zones), 1),
                "requiredSoc": home_required,
                "targetSoc": _soc_target(home_required),
                "modelName": "Final ML",
                "cleaningType": "물걸레" if mop_enabled else "건식",
                "cleaningTypeCode": 1 if mop_enabled else 0,
                "mopEnabled": mop_enabled,
                "obstacleLevel": "보통",
                "obstacleLevelCode": 2,
                "floorType": "혼합",
                "dirtLevel": "평균",
                "dirtCode": round(sum(z["dirtCode"] for z in zones) / len(zones), 3),
                "dirtMaxCode": max(z["dirtCode"] for z in zones),
                "suctionMode": "자동",
                "suctionCode": 2,
                "suctionMaxCode": 3,
                "needsRecharge": "무충전 완주 가능",
                "chargeCount": 0,
            }
            runs.append({
                "globalRunId": home["globalRunId"],
                "areaPyung": area,
                "zoneCount": zone_count,
                "mopEnabled": mop_enabled,
                "cleaningType": home["cleaningType"],
                "home": home,
                "zones": zones,
            })
    return runs


def _build_zone_from_final_row(zrow, idx):
    zone_no = _safe_int(zrow, ["zone"], idx)
    area_pyung = _safe_int(zrow, ["area_pyung"], 0)
    zone_count = _safe_int(zrow, ["zone_count"], 0)
    required = _safe_float(zrow, ["zone_soc_used_pct"], 0)
    target = _safe_float(zrow, ["zone_target_soc_pct"], _soc_target(required))
    mop_enabled = _infer_mop(zrow)
    cleaning_type = _safe_text(zrow, ["cleaning_type"], "물걸레" if mop_enabled else "건식")
    obstacle_code = _safe_float(zrow, ["obstacle_level_code"], 0)
    dirt_code = _safe_float(zrow, ["dirt_level_code"], 0)
    if not dirt_code:
        dirt_txt = _safe_text(zrow, ["dirt_level"], "")
        if "높" in dirt_txt or "많" in dirt_txt:
            dirt_code = 3
        elif "보통" in dirt_txt or "중" in dirt_txt:
            dirt_code = 2
        elif "낮" in dirt_txt or "적" in dirt_txt:
            dirt_code = 1
    suction_code = _safe_float(zrow, ["suction_mode_code"], 0)
    if not suction_code:
        suction_txt = _safe_text(zrow, ["effective_suction_mode"], "")
        if "터보" in suction_txt:
            suction_code = 4
        elif "강" in suction_txt:
            suction_code = 3
        elif "중" in suction_txt:
            suction_code = 2
        elif "약" in suction_txt:
            suction_code = 1

    return {
        "scope": "zone",
        "zone": zone_no,
        "label": f"{zone_no}구역",
        "globalRunId": _safe_text(zrow, ["global_run_id"], ""),
        "areaPyung": area_pyung,
        "zoneCount": zone_count,
        "cleaningAreaM2": round(_safe_float(zrow, ["zone_area_m2"], 0), 1),
        "requiredSoc": round(float(required), 1),
        "targetSoc": int(round(max(15, min(float(target), 90)))),
        "modelName": "Final ML",
        "cleaningType": cleaning_type,
        "cleaningTypeCode": 1 if mop_enabled else 0,
        "mopEnabled": mop_enabled,
        "obstacleLevel": _safe_text(zrow, ["obstacle_level"], ""),
        "obstacleLevelCode": round(float(obstacle_code), 3),
        "floorType": _safe_text(zrow, ["floor_type"], ""),
        "dirtLevel": _safe_text(zrow, ["dirt_level"], ""),
        "dirtCode": round(float(dirt_code), 3),
        "suctionMode": _safe_text(zrow, ["effective_suction_mode"], ""),
        "suctionCode": round(float(suction_code), 3),
        "zoneTimeMin": round(_safe_float(zrow, ["zone_time_min"], 0), 2),
        "zoneProgressPct": round(_safe_float(zrow, ["zone_progress_pct"], 0), 2),
        "socBeforeZone": round(_safe_float(zrow, ["soc_before_zone_pct"], 0), 2),
        "socAfterZone": round(_safe_float(zrow, ["soc_after_zone_pct"], 0), 2),
        "needsRecharge": _safe_text(zrow, ["needs_recharge"], ""),
        "chargeCount": _safe_int(zrow, ["charge_count"], 0),
        "isChargeZone": _safe_int(zrow, ["is_charge_zone"], 0),
        "firstChargeZone": _safe_int(zrow, ["first_charge_zone"], -1),
        "secondChargeZone": _safe_int(zrow, ["second_charge_zone"], -1),
        "firstChargeTargetSoc": round(_safe_float(zrow, ["first_charge_target_soc_pct"], 0), 2),
        "secondChargeTargetSoc": round(_safe_float(zrow, ["second_charge_target_soc_pct"], 0), 2),
    }


def _build_run_from_final_group(gid, zdf):
    zdf = zdf.copy()
    if "zone" in zdf.columns:
        zdf = zdf.sort_values("zone")

    zones = []
    for idx, (_, zrow) in enumerate(zdf.iterrows(), start=1):
        zones.append(_build_zone_from_final_row(zrow, idx))

    if not zones:
        return None

    first = zdf.iloc[0]
    area_pyung = _safe_int(first, ["area_pyung"], zones[0].get("areaPyung", 0))
    zone_count_from_csv = _safe_int(first, ["zone_count"], len(zones))
    zone_count = zone_count_from_csv or len(zones)
    mop_enabled = _infer_mop(first)
    cleaning_type = _safe_text(first, ["cleaning_type"], "물걸레" if mop_enabled else "건식")

    # 핵심 변경점:
    # 집 전체 필요 SOC는 각 zone의 zone_soc_used_pct 합산값입니다.
    # run_total_soc_pct가 있더라도 UI에서는 이 합산값을 우선 사용합니다.
    home_required = round(sum(float(z.get("requiredSoc", 0)) for z in zones), 1)
    home_target = _soc_target(home_required)

    dirt_values = [float(z.get("dirtCode", 0)) for z in zones if float(z.get("dirtCode", 0)) > 0]
    suction_values = [float(z.get("suctionCode", 0)) for z in zones if float(z.get("suctionCode", 0)) > 0]
    obstacle_values = [float(z.get("obstacleLevelCode", 0)) for z in zones if float(z.get("obstacleLevelCode", 0)) > 0]

    home = {
        "scope": "home",
        "label": "집 전체",
        "globalRunId": str(gid),
        "areaPyung": area_pyung,
        "zoneCount": zone_count,
        "cleaningAreaM2": round(sum(float(z.get("cleaningAreaM2", 0)) for z in zones), 1),
        "requiredSoc": home_required,
        "targetSoc": home_target,
        "modelName": "Final ML",
        "cleaningType": cleaning_type,
        "cleaningTypeCode": 1 if mop_enabled else 0,
        "mopEnabled": mop_enabled,
        "obstacleLevel": _safe_text(first, ["obstacle_level"], ""),
        "obstacleLevelCode": round(sum(obstacle_values) / len(obstacle_values), 3) if obstacle_values else 0,
        "floorType": "혼합",
        "dirtLevel": "평균",
        "dirtCode": round(sum(dirt_values) / len(dirt_values), 3) if dirt_values else 0,
        "dirtMaxCode": round(max(dirt_values), 3) if dirt_values else 0,
        "suctionMode": "자동",
        "suctionCode": round(sum(suction_values) / len(suction_values), 3) if suction_values else 0,
        "suctionMaxCode": round(max(suction_values), 3) if suction_values else 0,
        "runTotalSocFromCsv": round(_safe_float(first, ["run_total_soc_pct"], home_required), 3),
        "runTotalTimeMin": round(_safe_float(first, ["run_total_time_min"], 0), 2),
        "runEndSoc": round(_safe_float(first, ["run_end_soc_pct"], 0), 2),
        "needsRecharge": _safe_text(first, ["needs_recharge"], ""),
        "chargeCount": _safe_int(first, ["charge_count"], 0),
        "firstChargeZone": _safe_int(first, ["first_charge_zone"], -1),
        "secondChargeZone": _safe_int(first, ["second_charge_zone"], -1),
    }

    return {
        "globalRunId": str(gid),
        "areaPyung": area_pyung,
        "zoneCount": zone_count,
        "mopEnabled": mop_enabled,
        "cleaningType": cleaning_type,
        "home": home,
        "zones": zones,
    }




def _limit_final_ml_runs(ml_df, max_runs=96, per_bucket=4):
    """최종 ML CSV는 유지하되, Streamlit 화면으로 넘길 run 수만 제한합니다.

    50,000행 전체를 JS JSON으로 넣으면 HTML이 너무 커져 배포 환경에서 앱이 멈출 수 있습니다.
    소형/중형/대형, 건식/물걸레, 충전 필요 여부가 골고루 남도록 global_run_id 단위로 샘플링합니다.
    한 run의 zone들은 모두 같이 유지되므로 집 전체 SOC 합산 로직은 깨지지 않습니다.
    """
    if ml_df is None or len(ml_df) == 0 or "global_run_id" not in ml_df.columns:
        return ml_df

    df = ml_df.copy()
    df["global_run_id"] = df["global_run_id"].astype(str)

    agg = {"global_run_id": "first"}
    for col, fn in [
        ("area_pyung", "first"),
        ("zone_count", "first"),
        ("cleaning_type_code", "first"),
        ("cleaning_type", "first"),
        ("charge_count", "max"),
        ("run_total_soc_pct", "first"),
    ]:
        if col in df.columns:
            agg[col] = fn

    run_meta = df.groupby("global_run_id", sort=False).agg(agg)

    def _bucket_row(row):
        zone_count = int(row.get("zone_count", 0) or 0)
        if zone_count not in [4, 6, 8]:
            area = float(row.get("area_pyung", 0) or 0)
            zone_count = 4 if area <= 24 else (6 if area <= 49 else 8)

        mop = 0
        if "cleaning_type_code" in row.index and _is_valid(row.get("cleaning_type_code")):
            try:
                mop = int(round(float(row.get("cleaning_type_code"))))
            except Exception:
                mop = 0
        else:
            txt = str(row.get("cleaning_type", "")).lower()
            mop = 1 if any(k in txt for k in ["물", "걸레", "mop", "wet"]) else 0

        charge_flag = 1 if float(row.get("charge_count", 0) or 0) > 0 else 0
        return f"{zone_count}_{mop}_{charge_flag}"

    run_meta["_bucket"] = run_meta.apply(_bucket_row, axis=1)

    selected_ids = []
    for _, part in run_meta.groupby("_bucket", sort=True):
        if "run_total_soc_pct" in part.columns:
            part = part.sort_values("run_total_soc_pct")
        else:
            part = part.sort_index()

        if len(part) <= per_bucket:
            chosen = part.index.tolist()
        else:
            positions = [round(i * (len(part) - 1) / (per_bucket - 1)) for i in range(per_bucket)]
            chosen = part.iloc[positions].index.tolist()
        selected_ids.extend(chosen)

    selected_ids = list(dict.fromkeys(map(str, selected_ids)))
    if len(selected_ids) > max_runs:
        selected_ids = selected_ids[:max_runs]

    limited = df[df["global_run_id"].isin(selected_ids)].copy()

    if "zone_count" in df.columns:
        present = set(limited["zone_count"].dropna().astype(int).unique().tolist())
        source_counts = set(df["zone_count"].dropna().astype(int).unique().tolist())
        needed = [z for z in [4, 6, 8] if z not in present and z in source_counts]
        if needed:
            extra_ids = []
            for zc in needed:
                candidates = df[df["zone_count"].astype(int) == zc]["global_run_id"].drop_duplicates().astype(str).tolist()
                if candidates:
                    extra_ids.append(candidates[0])
            limited = df[df["global_run_id"].isin(selected_ids + extra_ids)].copy()

    return limited


def make_prediction_payload_from_final_ml(ml_df):
    runs = []
    if ml_df is not None and len(ml_df) > 0 and "global_run_id" in ml_df.columns:
        ml_df = ml_df.copy()
        ml_df["global_run_id"] = ml_df["global_run_id"].astype(str)
        for gid, zdf in ml_df.groupby("global_run_id", sort=False):
            run = _build_run_from_final_group(gid, zdf)
            if run is not None:
                runs.append(run)

    data_status = "final_ml_csv" if runs else "demo"
    if not runs:
        runs = _make_demo_runs()

    area_options = sorted({r["areaPyung"] for r in runs if r.get("areaPyung")})
    zone_count_options = sorted({r.get("zoneCount") for r in runs if r.get("zoneCount")})
    mop_values = sorted({bool(r["mopEnabled"]) for r in runs})
    default_run = runs[0]

    return {
        "currentSoc": int(CURRENT_SOC),
        "runs": runs,
        "areaOptions": area_options,
        "zoneCountOptions": zone_count_options,
        "defaultAreaPyung": default_run["areaPyung"],
        "defaultZoneCount": default_run.get("zoneCount", len(default_run.get("zones", []))),
        "defaultMopEnabled": bool(default_run["mopEnabled"]),
        "dataStatus": data_status,
        "homeSocRule": "sum_zone_soc_used_pct",
    }


# -----------------------------
# 예전 2파일 구조 fallback
# -----------------------------
def _build_home_scenario(home_row):
    required = _safe_float(
        home_row,
        ["best_pred_required_soc_pct", "pred_XGBoost", "pred_RandomForest", "home_required_soc_pct"],
        25,
    )
    target = _safe_float(
        home_row,
        ["best_pred_target_soc_pct", "home_target_soc_pct"],
        _soc_target(required),
    )
    mop_enabled = _infer_mop(home_row)
    cleaning_type = _safe_text(home_row, ["cleaning_type_first", "cleaning_type"], "물걸레" if mop_enabled else "건식")
    cleaning_type_code = int(round(_safe_float(home_row, ["cleaning_type_code_first", "cleaning_type_code"], 1 if mop_enabled else 0)))
    obstacle_code = _safe_float(home_row, ["obstacle_level_code_first", "obstacle_level_code"], 0)
    dirt_mean_code = _safe_float(home_row, ["dirt_level_code_mean", "dirt_level_code"], 0)
    dirt_max_code = _safe_float(home_row, ["dirt_level_code_max", "dirt_level_code"], dirt_mean_code)
    suction_mean_code = _safe_float(home_row, ["suction_mode_code_mean", "suction_mode_code"], 0)
    suction_max_code = _safe_float(home_row, ["suction_mode_code_max", "suction_mode_code"], suction_mean_code)
    zone_count = _safe_int(home_row, ["zone_count_first", "zone_count"], 0)
    return {
        "scope": "home",
        "label": "집 전체",
        "globalRunId": _safe_text(home_row, ["global_run_id"], ""),
        "areaPyung": int(round(_safe_float(home_row, ["area_pyung_first", "area_pyung"], 0))),
        "zoneCount": zone_count,
        "cleaningAreaM2": int(round(_safe_float(home_row, ["zone_area_m2_sum", "cleaning_area_m2"], 0))),
        "requiredSoc": round(float(required), 1),
        "targetSoc": int(round(max(15, min(float(target), 90)))),
        "modelName": _safe_text(home_row, ["best_model"], "XGBoost"),
        "cleaningType": cleaning_type,
        "cleaningTypeCode": cleaning_type_code,
        "mopEnabled": mop_enabled,
        "obstacleLevel": _safe_text(home_row, ["obstacle_level_first", "obstacle_level"], ""),
        "obstacleLevelCode": round(float(obstacle_code), 3),
        "floorType": "혼합",
        "dirtLevel": "평균",
        "dirtCode": round(float(dirt_mean_code), 3),
        "dirtMaxCode": round(float(dirt_max_code), 3),
        "suctionMode": "자동",
        "suctionCode": round(float(suction_mean_code), 3),
        "suctionMaxCode": round(float(suction_max_code), 3),
    }


def _build_zone_scenario(zrow, idx, home):
    zone_no = int(round(_safe_float(zrow, ["zone"], idx)))
    required = _safe_float(
        zrow,
        ["best_pred_required_soc_pct", "pred_RandomForest", "pred_XGBoost", "zone_required_soc_pct"],
        max(home["requiredSoc"] / 5, 1),
    )
    mop_enabled = _infer_mop(zrow)
    cleaning_type = _safe_text(zrow, ["cleaning_type"], home.get("cleaningType", ""))
    cleaning_type_code = int(round(_safe_float(zrow, ["cleaning_type_code"], 1 if mop_enabled else 0)))
    obstacle_code = _safe_float(zrow, ["obstacle_level_code"], home.get("obstacleLevelCode", 0))
    dirt_code = _safe_float(zrow, ["dirt_level_code"], 0)
    suction_code = _safe_float(zrow, ["suction_mode_code"], 0)
    return {
        "scope": "zone",
        "zone": zone_no,
        "label": f"{zone_no}구역",
        "globalRunId": _safe_text(zrow, ["global_run_id"], home["globalRunId"]),
        "areaPyung": int(round(_safe_float(zrow, ["area_pyung", "area_pyung_first"], home["areaPyung"]))),
        "zoneCount": int(home.get("zoneCount") or 0),
        "cleaningAreaM2": round(_safe_float(zrow, ["zone_area_m2"], 0), 1),
        "requiredSoc": round(float(required), 1),
        "targetSoc": _soc_target(required),
        "modelName": _safe_text(zrow, ["best_model"], "RandomForest"),
        "cleaningType": cleaning_type,
        "cleaningTypeCode": cleaning_type_code,
        "mopEnabled": mop_enabled,
        "obstacleLevel": _safe_text(zrow, ["obstacle_level"], home.get("obstacleLevel", "")),
        "obstacleLevelCode": round(float(obstacle_code), 3),
        "floorType": _safe_text(zrow, ["floor_type"], ""),
        "dirtLevel": _safe_text(zrow, ["dirt_level"], ""),
        "dirtCode": round(float(dirt_code), 3),
        "suctionMode": _safe_text(zrow, ["effective_suction_mode"], ""),
        "suctionCode": round(float(suction_code), 3),
    }


def make_prediction_payload(home_df, zone_df):
    runs = []

    if home_df is not None and len(home_df) > 0:
        for _, hrow in home_df.iterrows():
            home = _build_home_scenario(hrow)
            gid = home["globalRunId"]
            zones = []

            if zone_df is not None and "global_run_id" in zone_df.columns and gid:
                zdf = zone_df[zone_df["global_run_id"].astype(str) == str(gid)].copy()
                if "zone" in zdf.columns:
                    zdf = zdf.sort_values("zone")
                for idx, (_, zrow) in enumerate(zdf.iterrows(), start=1):
                    zone = _build_zone_scenario(zrow, idx, home)
                    zone["cleaningType"] = home["cleaningType"]
                    zone["mopEnabled"] = home["mopEnabled"]
                    zones.append(zone)

            if len(zones) >= 1:
                # fallback에서도 zone_count가 없으면 실제 zone 개수를 사용
                home["zoneCount"] = int(home.get("zoneCount") or len(zones))
                for z in zones:
                    z["zoneCount"] = home["zoneCount"]
                runs.append({
                    "globalRunId": gid,
                    "areaPyung": home["areaPyung"],
                    "zoneCount": home["zoneCount"],
                    "mopEnabled": home["mopEnabled"],
                    "cleaningType": home["cleaningType"],
                    "home": home,
                    "zones": zones,
                })

    if not runs and zone_df is not None and len(zone_df) > 0 and "global_run_id" in zone_df.columns:
        for gid, zdf in zone_df.groupby("global_run_id"):
            if len(zdf) < 1:
                continue
            if "zone" in zdf.columns:
                zdf = zdf.sort_values("zone")
            first = zdf.iloc[0]
            area = int(round(_safe_float(first, ["area_pyung"], 18)))
            mop_enabled = _infer_mop(first)
            dummy_home = {
                "scope": "home", "label": "집 전체", "globalRunId": str(gid), "areaPyung": area,
                "zoneCount": len(zdf),
                "cleaningAreaM2": int(round(zdf["zone_area_m2"].sum())) if "zone_area_m2" in zdf.columns else 0,
                "requiredSoc": 0, "targetSoc": 15, "modelName": "XGBoost",
                "cleaningType": "물걸레" if mop_enabled else "건식", "cleaningTypeCode": 1 if mop_enabled else 0, "mopEnabled": mop_enabled,
                "obstacleLevel": _safe_text(first, ["obstacle_level"], ""), "obstacleLevelCode": _safe_float(first, ["obstacle_level_code"], 0), "floorType": "혼합",
                "dirtLevel": "평균", "dirtCode": 0, "dirtMaxCode": 0, "suctionMode": "자동", "suctionCode": 0, "suctionMaxCode": 0
            }
            zones = []
            dummy_required = 0
            for idx, (_, zrow) in enumerate(zdf.iterrows(), start=1):
                zone = _build_zone_scenario(zrow, idx, dummy_home)
                dummy_required += zone["requiredSoc"]
                zones.append(zone)
            dummy_home["requiredSoc"] = round(dummy_required, 1)
            dummy_home["targetSoc"] = _soc_target(dummy_required)
            runs.append({
                "globalRunId": str(gid), "areaPyung": area, "zoneCount": len(zones), "mopEnabled": mop_enabled,
                "cleaningType": dummy_home["cleaningType"], "home": dummy_home, "zones": zones
            })

    data_status = "legacy_csv" if runs else "demo"
    if not runs:
        runs = _make_demo_runs()

    area_options = sorted({r["areaPyung"] for r in runs if r.get("areaPyung")})
    zone_count_options = sorted({r.get("zoneCount") for r in runs if r.get("zoneCount")})
    mop_values = sorted({bool(r["mopEnabled"]) for r in runs})
    default_run = runs[0]

    return {
        "currentSoc": int(CURRENT_SOC),
        "runs": runs,
        "areaOptions": area_options,
        "zoneCountOptions": zone_count_options,
        "defaultAreaPyung": default_run["areaPyung"],
        "defaultZoneCount": default_run.get("zoneCount", len(default_run.get("zones", []))),
        "defaultMopEnabled": bool(default_run["mopEnabled"]),
        "dataStatus": data_status,
    }


ml_output_path = _first_existing_csv([ML_OUTPUT_PATH, ML_OUTPUT_ALT_PATH])
ml_output_df = load_prediction_csv(str(ml_output_path)) if ml_output_path else None

if ml_output_df is not None:
    ui_prediction_data = make_prediction_payload_from_final_ml(ml_output_df)
else:
    home_pred_df = load_prediction_csv(str(HOME_PRED_PATH))
    zone_pred_df = load_prediction_csv(str(ZONE_PRED_PATH))
    ui_prediction_data = make_prediction_payload(home_pred_df, zone_pred_df)

UI_PREDICTION_JSON = json.dumps(ui_prediction_data, ensure_ascii=False)

ui_media_data = {
    "photos": load_image_folder(str(PHOTO_DIR), _folder_signature(PHOTO_DIR)),
    "lostItems": load_image_folder(str(LOST_DIR), _folder_signature(LOST_DIR)),
}
UI_MEDIA_JSON = json.dumps(ui_media_data, ensure_ascii=False)

# 크리스마스 에디션 산타 모자 아이콘을 코드에 내장해 별도 이미지 파일 없이 동작합니다.
SANTA_HAT_DATA_URI = 'data:image/png;base64,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'


APP_HTML = r"""
<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{
  --brown:#4b3324;--brown2:#735139;--cream:#fff8e8;--green:#62aa49;
  --green2:#2f8b3a;--orange:#ff9535;--red:#ef4e45;--yellow:#ffd44f;
  --shadow:0 8px 18px rgba(72,44,20,.15)
}
html,body{margin:0;min-height:100%;font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",Arial,sans-serif;color:var(--brown);background:transparent}
body{display:flex;justify-content:center;align-items:flex-start;padding:8px}
button,input,select{font-family:inherit} button{cursor:pointer}
.phone{position:relative;width:min(100%,420px);height:960px;overflow:hidden;border:8px solid #242321;border-radius:40px;background:#dfb46b;box-shadow:0 30px 80px rgba(50,33,18,.28),0 8px 20px rgba(50,33,18,.16)}
.notch{position:absolute;z-index:100;top:0;left:50%;width:126px;height:25px;transform:translateX(-50%);border-radius:0 0 18px 18px;background:#242321}
.screen{position:relative;width:100%;height:100%;overflow:hidden;background:linear-gradient(180deg,#d2ab7b 0%,#e8c793 44%,#e1b36c 100%)}

/* Header */
.header{position:relative;z-index:50;height:128px;padding:23px 14px 8px;color:#fff;background:linear-gradient(120deg,#2d2722,#5b3f2d);box-shadow:0 7px 16px rgba(48,31,19,.22)}
.header-top{display:flex;justify-content:space-between;align-items:center}
.brand{font-size:9px;font-weight:900;letter-spacing:1.4px}
.app-title{margin-top:3px;font-size:23px;font-weight:900}
.coin-pill{display:flex;align-items:center;gap:5px;padding:8px 12px;border:1px solid rgba(255,255,255,.17);border-radius:18px;background:rgba(255,255,255,.13);font-size:12px;font-weight:900}
.nav{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:12px}
.nav-btn{padding:8px 3px;border:0;border-radius:14px;background:transparent;color:rgba(255,255,255,.72);font-size:10px;font-weight:900;transition:.2s}
.nav-btn.active{background:#4d291c;color:#fff;box-shadow:0 4px 9px rgba(0,0,0,.18)}
.nav-btn:active{transform:scale(.95)}

/* Pages */
.pages{position:relative;height:calc(100% - 128px);overflow:hidden}
.page{position:absolute;inset:0;display:none;overflow-y:auto;padding:12px 10px 24px;animation:pageIn .25s ease-out}
.page.active{display:block}.page::-webkit-scrollbar{width:0}
@keyframes pageIn{from{opacity:0;transform:translateX(16px)}to{opacity:1;transform:none}}
.section-kicker{color:#76533b;font-size:9px;font-weight:900;letter-spacing:1.3px}
.section-title{margin:2px 0 11px;font-size:22px;font-weight:900}
.panel{border:1px solid rgba(136,87,40,.14);border-radius:17px;background:rgba(255,248,231,.96);box-shadow:var(--shadow)}

/* Home */
#homePage{padding:0;background:linear-gradient(180deg,#cfaa7d 0%,#e0c39a 39%,#d29c58 40%,#d09850 100%)}
.room{position:relative;height:355px;overflow:hidden}
.wall-light{position:absolute;top:-80px;left:50%;width:420px;height:280px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(circle,rgba(255,248,226,.88),rgba(255,240,205,.18) 60%,transparent 74%)}
.floor{position:absolute;left:0;right:0;bottom:0;height:170px;background:repeating-linear-gradient(90deg,rgba(106,63,26,.1) 0,rgba(106,63,26,.1) 2px,transparent 2px,transparent 66px),repeating-linear-gradient(0deg,transparent 0,transparent 38px,rgba(106,63,26,.09) 39px,rgba(106,63,26,.09) 41px),linear-gradient(180deg,#d9b174,#c78e48)}
.plant{position:absolute;z-index:3;left:14px;top:70px;font-size:74px;filter:drop-shadow(0 7px 5px rgba(68,41,21,.18))}
.house{position:absolute;z-index:3;left:88px;top:128px;width:68px;height:58px;border-radius:29px 29px 7px 7px;background:linear-gradient(145deg,#a38b71,#74614d);box-shadow:0 6px 11px rgba(54,36,23,.22)}
.house:before{content:"";position:absolute;left:19px;bottom:0;width:31px;height:32px;border-radius:16px 16px 0 0;background:#403b35}
.house:after{content:"HOME";position:absolute;top:11px;left:16px;color:rgba(255,255,255,.56);font-size:7px;font-weight:900}
.sofa{position:absolute;z-index:2;right:-8px;top:72px;width:139px;height:105px;border-radius:28px 0 8px 8px;background:linear-gradient(145deg,#71847f,#354e4a);box-shadow:0 10px 14px rgba(54,37,23,.27)}
.sofa:before{content:"";position:absolute;top:-18px;left:10px;width:80px;height:48px;border-radius:17px 17px 7px 7px;background:#74867f}
.speech{position:absolute;z-index:20;top:17px;left:50%;width:177px;min-height:74px;padding:14px 12px;transform:translateX(-50%);border-radius:14px;background:rgba(255,255,255,.98);box-shadow:0 7px 16px rgba(58,37,21,.18);text-align:center;font-size:12px;line-height:1.55;font-weight:800}
.speech strong{color:var(--green);font-size:14px}
.speech:after{content:"";position:absolute;left:52%;bottom:-15px;border-width:16px 10px 0 4px;border-style:solid;border-color:white transparent transparent transparent}
.mode-chip{position:absolute;z-index:18;top:106px;left:50%;padding:7px 13px;transform:translateX(-50%);border-radius:18px;background:rgba(255,248,229,.95);box-shadow:0 4px 10px rgba(72,46,23,.16);font-size:9px;font-weight:900}
.rug{position:absolute;z-index:4;left:50%;bottom:12px;width:255px;height:92px;transform:translateX(-50%);border-radius:50%;background:radial-gradient(ellipse,rgba(241,224,197,.91),rgba(191,151,103,.79));box-shadow:inset 0 0 18px rgba(103,70,43,.14)}
.clean-path{position:absolute;z-index:5;left:50%;bottom:41px;width:292px;height:78px;transform:translateX(-50%);overflow:hidden;border:2px dashed rgba(255,255,255,.36);border-radius:50%;opacity:0}
.clean-fill{width:0;height:100%;border-radius:inherit;background:linear-gradient(90deg,rgba(95,177,105,.08),rgba(102,200,115,.51));transition:width .3s}
.charge-ring{position:absolute;z-index:7;left:50%;bottom:19px;width:216px;height:132px;transform:translateX(-50%);border:5px solid transparent;border-top-color:#ffd345;border-right-color:#ff9931;border-radius:50%;opacity:0}
.dust{position:absolute;z-index:8;left:50%;bottom:55px;width:267px;height:75px;transform:translateX(-50%);pointer-events:none}
.dust span{position:absolute;bottom:0;width:7px;height:7px;border-radius:50%;background:rgba(116,78,42,.5);opacity:0}
.dust span:nth-child(1){left:8%}.dust span:nth-child(2){left:21%;animation-delay:.32s}.dust span:nth-child(3){left:37%;animation-delay:.68s}.dust span:nth-child(4){right:8%;animation-delay:.18s}.dust span:nth-child(5){right:23%;animation-delay:.52s}.dust span:nth-child(6){right:39%;animation-delay:.88s}
.robot{position:absolute;z-index:10;left:50%;bottom:31px;width:181px;height:99px;transform:translateX(-50%);transform-origin:center bottom;border:2px solid #a29b92;border-radius:62% 62% 40% 40%;background:linear-gradient(180deg,#fffefb 0%,#e7e8e3 70%,#bbbdb7 100%);box-shadow:0 13px 19px rgba(55,37,21,.32),inset 0 -8px 12px rgba(83,83,79,.12);cursor:pointer;animation:robotIdle 2.8s ease-in-out infinite}
.robot-top{position:absolute;left:50%;top:-5px;width:126px;height:58px;transform:translateX(-50%);border-top:2px solid rgba(119,119,114,.42);border-radius:50%;background:radial-gradient(ellipse at center,#fbfbf8 0%,#d5d6d2 74%,#b8b9b3 100%)}
.face{position:absolute;z-index:3;left:50%;bottom:8px;width:128px;height:54px;transform:translateX(-50%);border-radius:26px 26px 30px 30px;background:linear-gradient(180deg,#2a2c2d,#101213 76%);box-shadow:inset 0 4px 5px rgba(255,255,255,.13)}
.eye{position:absolute;top:14px;width:22px;height:22px;border:2px solid #f2f0dc;border-radius:50%;background:#111;transform-origin:center;animation:blink 4.8s infinite}
.eye:after{content:"";position:absolute;top:4px;left:5px;width:7px;height:7px;border-radius:50%;background:#fff;transition:transform .25s}
.eye.left{left:20px}.eye.right{right:20px}.robot.look-left .eye:after{transform:translateX(-4px)}.robot.look-right .eye:after{transform:translateX(4px)}
.cheek{position:absolute;bottom:8px;width:13px;height:6px;border-radius:50%;background:#ff8d8d;opacity:.75}.cheek.left{left:8px}.cheek.right{right:8px}
.mouth{position:absolute;left:50%;bottom:8px;width:20px;height:11px;transform:translateX(-50%);border:2px solid #f3d6c9;border-top:0;border-radius:0 0 12px 12px}
.crown{position:absolute;z-index:12;left:50%;top:-40px;transform:translateX(-50%);font-size:46px;filter:drop-shadow(0 4px 3px rgba(81,52,17,.25))}
.spark{position:absolute;z-index:11;right:-16px;top:-9px;font-size:28px;animation:sparkle 1.3s ease-in-out infinite}
.slot{position:absolute;left:50%;bottom:-2px;width:43px;height:5px;transform:translateX(-50%);border-radius:10px;background:#484a48}
.effect-layer{position:absolute;z-index:25;inset:0;overflow:hidden;pointer-events:none}.effect{position:absolute;left:50%;top:68%;font-size:20px;animation:effectFly 1.2s ease-out forwards}
.room.cleaning .mode-chip{color:#fff;background:rgba(57,143,82,.93)}.room.cleaning .clean-path{opacity:1}.room.cleaning .dust span{animation:dustRise 1.35s ease-out infinite}.room.cleaning .robot{animation:robotPatrol 2.4s ease-in-out infinite}
.room.charging .mode-chip{color:#fff;background:rgba(242,145,35,.94)}.room.charging .charge-ring{opacity:.92;animation:ringSpin 1.05s linear infinite}.room.charging .robot{animation:robotCharge .85s ease-in-out infinite}
.room.low .robot{animation:robotLow .48s linear infinite}.room.celebrate .robot{animation:robotCelebrate .72s ease-in-out 3}.robot.tap{animation:robotTap .62s ease-out!important}
.mission{position:absolute;z-index:16;left:8px;bottom:14px;width:90px;padding:9px 7px;border-radius:14px;background:rgba(255,248,230,.97);box-shadow:0 4px 10px rgba(61,39,20,.22)}
.mission-title{font-size:10px;font-weight:900}.mission-text{margin-top:5px;font-size:9px;line-height:1.4;font-weight:800}.mission-progress{display:flex;align-items:center;gap:4px;margin-top:8px}.mission-track{flex:1;height:7px;overflow:hidden;border-radius:10px;background:#c9b794}.mission-fill{width:0;height:100%;border-radius:inherit;background:linear-gradient(90deg,#ff8e33,#ffca43);transition:width .3s}.reward-small{color:#8d5814;font-size:9px;font-weight:900}
.quick{position:absolute;z-index:17;right:7px;top:89px;display:flex;flex-direction:column;gap:8px}.quick-btn{width:52px;min-height:51px;padding:4px 2px;border:0;border-radius:15px;background:rgba(255,248,231,.97);box-shadow:0 4px 10px rgba(61,39,20,.22);color:var(--brown);font-size:8px;font-weight:900}.quick-btn .icon{display:block;margin-bottom:3px;font-size:21px}
.home-dashboard{padding:9px 8px 15px;background:linear-gradient(180deg,rgba(239,205,151,.99),rgba(227,181,110,.99))}
.actions{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin-bottom:8px;padding:8px 5px;border:1px solid rgba(138,91,40,.18);border-radius:14px;background:rgba(255,247,224,.94);box-shadow:0 4px 9px rgba(87,54,25,.15)}
.action-btn{min-width:0;padding:3px 0;border:0;background:transparent;color:var(--brown);font-size:8px;font-weight:900}.action-icon{display:block;margin-bottom:4px;font-size:23px}
.home-cards{display:grid;grid-template-columns:1.16fr 1fr .78fr;gap:6px}.mini-card{min-height:186px;padding:11px 9px;border:1px solid rgba(139,92,39,.17);border-radius:14px;background:rgba(255,248,230,.97);box-shadow:0 4px 10px rgba(79,48,21,.12)}
.mini-title{margin-bottom:8px;font-size:10px;font-weight:900}.battery-info{font-size:9px;line-height:1.55;font-weight:800}.battery-face{margin:7px 0 5px;text-align:center;font-size:31px}
.scale{position:relative;height:7px;margin:18px 7px 14px;border-radius:10px;background:linear-gradient(90deg,#f15b44 0%,#ffd25c 44%,#76ad51 100%)}.pointer{position:absolute;top:-7px;left:81%;width:14px;height:14px;transform:translateX(-50%);border:3px solid #fff;border-radius:50%;background:#e64c39;box-shadow:0 2px 5px rgba(0,0,0,.23);transition:left .3s}
.scale-labels{display:flex;justify-content:space-between;font-size:7px;font-weight:900}.battery-message{margin-top:10px;padding:7px;border-radius:9px;background:#f1e4c6;font-size:8px;line-height:1.45;font-weight:800}
.time-card{text-align:center}.time-icon{margin-top:10px;font-size:31px;animation:float 2s ease-in-out infinite}.time-number{color:#ef573f;font-size:32px;line-height:1;font-weight:900}.time-number small{font-size:12px}.time-sub{margin-top:4px;font-size:8px;font-weight:800}.time-tip{margin-top:15px;padding:7px 5px;border-radius:9px;background:#fff0ca;color:#745431;font-size:8px;line-height:1.45;font-weight:800}
.food-card{display:flex;flex-direction:column;align-items:center;justify-content:space-between}.food-title{width:100%;font-size:10px;font-weight:900}.food-bowl{position:relative;width:64px;height:42px;margin:26px auto 10px;border-radius:6px 6px 25px 25px;background:linear-gradient(180deg,#d84849,#ad2e36);box-shadow:0 7px 8px rgba(81,37,25,.2),inset 0 -7px 8px rgba(83,12,22,.14)}
.food-bowl:before{content:"";position:absolute;left:4px;top:-9px;width:56px;height:19px;border:4px solid #d54749;border-radius:50%;background:radial-gradient(circle at 30% 35%,#f1ab36 0 4px,transparent 5px),radial-gradient(circle at 60% 45%,#d57d24 0 5px,transparent 6px),radial-gradient(circle at 78% 30%,#f3c248 0 4px,transparent 5px),#944827}.food-bowl:after{content:"⚡";position:absolute;left:50%;top:10px;transform:translateX(-50%);color:#ffd542;font-size:20px;font-weight:900}.food-count{font-size:9px;font-weight:900}


/* 맞춤 배터리 Plan Selector */
.plan-panel{margin-bottom:8px;padding:11px 10px;background:rgba(255,248,231,.98)}
.plan-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.plan-title{font-size:11px;font-weight:900}.plan-model{padding:4px 7px;border-radius:11px;background:#eaf4df;color:#367b36;font-size:8px;font-weight:900}
.scope-buttons{display:grid;grid-template-columns:1.05fr repeat(5,1fr);gap:5px;margin-bottom:8px}
.scope-btn{min-height:37px;padding:5px 2px;border:1px solid rgba(124,83,43,.16);border-radius:12px;background:#f3e2be;color:#5a412e;font-size:8px;font-weight:900;line-height:1.2;box-shadow:0 3px 7px rgba(69,43,20,.09)}
.scope-btn.active{background:linear-gradient(180deg,#65ae4b,#368e3d);color:#fff;border-color:transparent;box-shadow:0 5px 12px rgba(47,139,58,.25)}
.learn-panel{position:relative;z-index:40;margin-bottom:8px;padding:9px;border-radius:13px;background:linear-gradient(145deg,#fff8df,#f3dfb2);border:1px solid rgba(124,83,43,.13)}.learn-top{display:flex;justify-content:space-between;align-items:center;gap:8px}.learn-title{font-size:10px;font-weight:900}.learn-pill{padding:4px 7px;border-radius:11px;background:#fff;color:#8b6139;font-size:8px;font-weight:900}.learn-desc{margin-top:5px;color:#6f4f38;font-size:8px;line-height:1.45;font-weight:800}.learn-progress{height:8px;margin-top:7px;overflow:hidden;border-radius:12px;background:#dcc79f}.learn-fill{width:0;height:100%;border-radius:inherit;background:linear-gradient(90deg,#62aa49,#ffd44f);transition:width .25s}.learn-status{margin-top:6px;font-size:8px;line-height:1.45;font-weight:900;color:#4b3324}.learn-steps{display:grid;grid-template-columns:1fr 1fr;gap:4px;margin-top:7px}.learn-step{padding:5px 4px;border-radius:9px;background:rgba(255,255,255,.58);color:#806047;font-size:7px;font-weight:900;text-align:center}.learn-step.done{background:#e7f4d9;color:#2f8b3a}.learn-step.active{background:#fff;color:#ef8c32;box-shadow:0 2px 6px rgba(89,56,26,.12)}.learn-btn{position:relative;z-index:80;pointer-events:auto!important;width:100%;min-height:34px;margin-top:7px;border:0;border-radius:11px;background:linear-gradient(90deg,#ef8c32,#ffb24b);color:#fff;font-size:10px;font-weight:900;box-shadow:0 5px 10px rgba(239,140,50,.22)}.learn-btn.ready{background:linear-gradient(90deg,#4a9b42,#75b84e)}.locked-area{opacity:.45;filter:grayscale(.15)}.condition-panel{margin-bottom:8px;padding:8px;border-radius:13px;background:#fff2cf;border:1px solid rgba(124,83,43,.12)}
.condition-title{margin-bottom:7px;font-size:10px;font-weight:900;color:#6f4f38;line-height:1.4}
.condition-row{display:grid;grid-template-columns:.7fr 1fr .7fr 1fr;gap:6px;align-items:center}.condition-row label{font-size:9px;font-weight:900;color:#6c4a2f}.condition-select{width:100%;min-height:34px;border:1px solid rgba(124,83,43,.22);border-radius:10px;background:#fffaf0;color:#4b3324;font-size:10px;font-weight:900;padding:0 7px}.predict-condition-grid{display:grid;grid-template-columns:.72fr 1fr .72fr 1fr;gap:6px;align-items:center;margin-top:8px}.predict-condition-grid label{font-size:9px;font-weight:900;color:#6c4a2f;white-space:nowrap}.condition-help{font-size:9px;line-height:1.5;color:#8a6a45;margin:7px 0 0;font-weight:800}.first-learn-note{padding:8px 9px;border-radius:11px;background:rgba(255,255,255,.58);font-size:10px;line-height:1.55;color:#6f4f38}.predict-btn{width:100%;min-height:36px;margin-top:8px;border:0;border-radius:11px;background:linear-gradient(90deg,#4a9b42,#75b84e);color:#fff;font-size:11px;font-weight:900;box-shadow:0 5px 10px rgba(47,139,58,.2)}.predict-loading{margin-top:6px;min-height:18px;font-size:9px;line-height:1.45;color:#745431;font-weight:800}.predict-loading.active{color:#2f8b3a}
.selected-plan{display:grid;grid-template-columns:1fr .9fr;gap:7px;align-items:stretch}.plan-summary{padding:9px;border-radius:12px;background:#fff4d5;font-size:9px;line-height:1.55;font-weight:800}.plan-summary strong{color:#2f8b3a}.plan-soc{padding:9px;border-radius:12px;background:#f0e0be;text-align:center;font-weight:900}.plan-soc-label{font-size:8px;color:#79583e}.plan-soc-value{margin-top:2px;color:#ef573f;font-size:22px;line-height:1}.plan-soc-sub{margin-top:4px;font-size:8px;color:#76553e;line-height:1.35}.start-clean-primary{width:100%;min-height:46px;margin-top:9px;border:0;border-radius:14px;background:linear-gradient(90deg,#ef8c32,#f2a84d);color:#fff;font-size:13px;font-weight:950;letter-spacing:-.2px;box-shadow:0 7px 15px rgba(239,140,50,.26)}.start-clean-primary:disabled{opacity:.55;filter:grayscale(.12);box-shadow:none}.start-clean-primary small{display:block;margin-top:2px;font-size:9px;font-weight:800;color:rgba(255,255,255,.88)}

/* 공용 패널 헤더/기록 목록 (부품 케어 페이지에서 사용) */
.panel-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}.panel-title{font-size:13px;font-weight:900}.badge{padding:5px 8px;border-radius:12px;background:#fff0ce;color:#805c35;font-size:8px;font-weight:900}
.events{margin-top:9px;padding:15px 14px}.event-item{display:grid;grid-template-columns:43px 1fr;gap:8px;padding:11px 0;border-bottom:1px solid rgba(122,87,51,.12)}.event-item:last-child{border-bottom:0}.event-time{color:#946c43;font-size:9px;font-weight:900}.event-content strong{display:block;margin-bottom:3px;font-size:10px}.event-content span{color:#785a43;font-size:9px;line-height:1.4;font-weight:700}

/* Reward */
.level-panel{padding:18px 15px 20px;text-align:center;background:linear-gradient(145deg,#fff3cc,#ffd98a);display:flex;flex-direction:column;align-items:center}.level-robot{font-size:72px;animation:float 2s ease-in-out infinite}.level-number{width:100%;margin-top:4px;font-size:25px;font-weight:900;text-align:center}.level-track{width:calc(100% - 20px);height:11px;margin:12px 10px 5px;overflow:hidden;border-radius:10px;background:rgba(126,85,39,.18)}.level-fill{width:55%;height:100%;border-radius:inherit;background:linear-gradient(90deg,#ff7f35,#ffd244)}.level-caption{width:100%;font-size:9px;font-weight:900;text-align:center}
.reward-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:9px;align-items:stretch}
.reward-card{min-height:176px;padding:14px;border:1px solid rgba(136,87,40,.14);border-radius:16px;background:rgba(255,248,231,.97);box-shadow:var(--shadow);text-align:center;display:flex;flex-direction:column;align-items:center}
.reward-icon{font-size:38px;line-height:1}
.reward-title{margin-top:7px;font-size:11px;font-weight:900;min-height:15px;display:flex;align-items:center;justify-content:center}
.reward-desc{margin-top:4px;color:#775943;font-size:8px;line-height:1.4;font-weight:800;min-height:24px;display:flex;align-items:flex-start;justify-content:center}
.reward-status{min-height:15px;margin-top:4px;font-size:8.5px;font-weight:950;color:#2f8b3a;display:flex;align-items:center;justify-content:center}
.reward-btn{width:100%;margin-top:auto;padding:8px;border:0;border-radius:10px;background:#f0dfbc;color:#5c422f;font-size:9px;font-weight:900;min-height:33px}

/* Modal */
.modal{position:absolute;z-index:200;inset:0;display:none;align-items:center;justify-content:center;padding:30px;background:rgba(45,33,23,.62);backdrop-filter:blur(4px)}.modal.show{display:flex}.modal-card{width:100%;padding:19px;border-radius:20px;background:#fff8e8;box-shadow:0 18px 45px rgba(28,19,12,.38);animation:popup .18s ease-out}.modal-title{font-size:18px;font-weight:900}.modal-body{margin:13px 0 17px;color:#6c513c;font-size:12px;line-height:1.65;font-weight:700}.modal-actions{display:grid;grid-template-columns:1fr 1fr;gap:9px}.modal-btn{width:100%;padding:11px;border:0;border-radius:12px;font-weight:900}.modal-secondary{background:#efe1c8;color:#5c422f}.modal-primary{background:#ef8c32;color:#fff}.modal-actions.single{grid-template-columns:1fr}.modal-actions.single .modal-secondary{display:none}
.toast{position:absolute;z-index:220;left:50%;bottom:25px;width:max-content;max-width:84%;padding:11px 17px;transform:translateX(-50%) translateY(30px);border-radius:18px;background:rgba(44,37,31,.95);color:#fff;font-size:11px;font-weight:800;opacity:0;pointer-events:none;transition:.25s}.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

/* ===== Battery coach popup: happy winking Home Genie illustration ===== */
.battery-coach-copy{
  color:#6c513c;
  font-size:14px;
  line-height:1.65;
  font-weight:600;
  text-align:left;
  word-break:keep-all;
  overflow-wrap:break-word;
}
.battery-coach-copy p{margin:0 0 13px;}
.battery-coach-copy p:last-child{margin-bottom:0;}
.battery-coach-copy b{color:#4b3324;font-weight:800;}
.battery-coach-visual{
  position:relative;
  margin-top:17px;
  padding:6px 2px 2px;
  min-height:225px;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:flex-end;
}
.coach-speech{
  position:relative;
  z-index:5;
  width:min(100%,292px);
  margin:0 auto 18px;
  padding:13px 16px 14px;
  border:2px solid rgba(121,83,49,.10);
  border-radius:19px;
  background:#fff;
  box-shadow:0 8px 18px rgba(65,41,23,.14);
  color:#513827;
  font-size:13.5px;
  line-height:1.55;
  font-weight:900;
  text-align:center;
  letter-spacing:-.15px;
}
.coach-speech b{color:#2f8b3a;font-weight:1000;}
.coach-speech .coach-heart{color:#ef4e45;font-size:18px;vertical-align:-1px;}
.coach-speech:after{
  content:"";
  position:absolute;
  left:50%;
  bottom:-15px;
  width:22px;
  height:22px;
  transform:translateX(-50%) rotate(45deg);
  background:#fff;
  border-right:2px solid rgba(121,83,49,.08);
  border-bottom:2px solid rgba(121,83,49,.08);
  border-radius:0 0 5px 0;
}
.coach-robo-stage{
  position:relative;
  width:220px;
  height:110px;
  display:grid;
  place-items:end center;
}
.coach-robo-shadow{
  position:absolute;
  left:50%;
  bottom:2px;
  width:150px;
  height:18px;
  transform:translateX(-50%);
  border-radius:50%;
  background:rgba(73,48,28,.17);
  filter:blur(2px);
}
.coach-robo{
  position:absolute;
  left:50%;
  bottom:10px;
  width:154px;
  height:84px;
  transform:translateX(-50%);
  border:2px solid #aaa7a0;
  border-radius:58% 58% 39% 39%;
  background:linear-gradient(180deg,#fffefb 0%,#eeeeea 68%,#c7c8c2 100%);
  box-shadow:0 12px 18px rgba(55,37,21,.22),inset 0 -7px 10px rgba(83,83,79,.11);
  animation:coachHappyBob 1.8s ease-in-out infinite;
}
.coach-robo-top{
  position:absolute;
  left:50%;
  top:-6px;
  width:108px;
  height:49px;
  transform:translateX(-50%);
  border-top:2px solid rgba(119,119,114,.42);
  border-radius:50%;
  background:radial-gradient(ellipse at center,#fbfbf8 0%,#d8d9d5 74%,#b8b9b3 100%);
}
.coach-robo-face{
  position:absolute;
  z-index:3;
  left:50%;
  bottom:8px;
  width:110px;
  height:46px;
  transform:translateX(-50%);
  border-radius:23px 23px 28px 28px;
  background:linear-gradient(180deg,#2a2c2d,#101213 76%);
  box-shadow:inset 0 4px 5px rgba(255,255,255,.13);
}
.coach-eye-open{
  position:absolute;
  top:11px;
  right:22px;
  width:20px;
  height:20px;
  border:2px solid #f2f0dc;
  border-radius:50%;
  background:#111;
}
.coach-eye-open:after{
  content:"";
  position:absolute;
  top:4px;
  left:5px;
  width:6px;
  height:6px;
  border-radius:50%;
  background:#fff;
}
.coach-eye-wink{
  position:absolute;
  top:18px;
  left:21px;
  width:22px;
  height:10px;
  border-top:3px solid #f2f0dc;
  border-radius:50% 50% 0 0;
  transform:rotate(-8deg);
}
.coach-cheek{
  position:absolute;
  bottom:7px;
  width:13px;
  height:6px;
  border-radius:50%;
  background:#ff8d8d;
  opacity:.88;
}
.coach-cheek.left{left:7px}.coach-cheek.right{right:7px}
.coach-smile{
  position:absolute;
  left:50%;
  bottom:7px;
  width:25px;
  height:13px;
  transform:translateX(-50%);
  border:2px solid #f5ddd4;
  border-top:0;
  border-radius:0 0 15px 15px;
}
.coach-smile:after{
  content:"";
  position:absolute;
  left:50%;
  bottom:-1px;
  width:10px;
  height:4px;
  transform:translateX(-50%);
  border-radius:5px 5px 8px 8px;
  background:#f3949c;
  opacity:.9;
}
.coach-sparkle{
  position:absolute;
  z-index:6;
  color:#ffd44f;
  font-size:25px;
  line-height:1;
  text-shadow:0 3px 6px rgba(117,79,18,.18);
  animation:coachSparkle 1.35s ease-in-out infinite;
}
.coach-sparkle.s1{left:20px;bottom:61px;animation-delay:.1s;}
.coach-sparkle.s2{right:22px;bottom:74px;animation-delay:.48s;font-size:20px;}
.coach-sparkle.s3{right:44px;bottom:31px;animation-delay:.82s;font-size:16px;}
@keyframes coachHappyBob{
  0%,100%{transform:translateX(-50%) translateY(0) rotate(-1deg)}
  50%{transform:translateX(-50%) translateY(-6px) rotate(1deg)}
}
@keyframes coachSparkle{
  0%,100%{opacity:.45;transform:scale(.78) rotate(-12deg)}
  50%{opacity:1;transform:scale(1.16) rotate(10deg)}
}
@media(max-width:360px){
  .battery-coach-copy{font-size:14px;line-height:1.62;}
  .battery-coach-visual{min-height:205px;margin-top:13px;}
  .coach-speech{font-size:12.8px;padding:12px 13px;margin-bottom:16px;}
  .coach-robo-stage{height:100px;}
  .coach-robo{width:146px;height:80px;}
}

/* ===== Christmas limited reward: Santa hat ===== */
.reward-card.seasonal-card{
  position:relative;
  overflow:hidden;
  border-color:rgba(194,64,48,.25)!important;
  background:linear-gradient(145deg,#fff9e9,#fff0dd)!important;
}
.reward-card.seasonal-card:before{
  content:"CHRISTMAS";
  position:absolute;
  top:8px;
  right:8px;
  padding:3px 7px;
  border-radius:999px;
  background:#c94035;
  color:#fff;
  font-size:8px;
  line-height:1;
  font-weight:1000;
  letter-spacing:.5px;
}
.reward-icon.santa-reward-icon{
  width:52px;
  height:52px;
  margin:0 auto;
  display:grid;
  place-items:center;
  border-radius:15px;
  background:#eee1cf;
  box-shadow:inset 0 0 0 1px rgba(110,76,48,.08);
}
.santa-reward-icon img{width:35px;height:47px;object-fit:contain;display:block;}
.robot-head-deco.santa{
  top:-49px;
  width:116px;
  min-width:116px;
  height:74px;
  transform:translateX(-50%) rotate(-5deg);
}
.robot-head-deco.santa.show{display:block;animation:santaHatPop .34s ease-out;}
.robot-head-deco.santa .santa-cap{
  position:absolute;
  left:28px;
  top:7px;
  width:62px;
  height:46px;
  border-radius:46px 30px 9px 9px;
  background:linear-gradient(145deg,#e84f41 0%,#c5322d 72%,#9f2826 100%);
  transform:rotate(-10deg) skewX(-7deg);
  box-shadow:0 4px 5px rgba(76,38,25,.18);
}
.robot-head-deco.santa .santa-cap:after{
  content:"";
  position:absolute;
  right:-18px;
  top:-1px;
  width:31px;
  height:31px;
  border-radius:50%;
  background:#fffdf8;
  box-shadow:0 3px 5px rgba(75,50,33,.13);
}
.robot-head-deco.santa .santa-brim{
  position:absolute;
  left:20px;
  bottom:8px;
  width:78px;
  height:22px;
  border-radius:18px;
  background:linear-gradient(180deg,#fff 0%,#f2eee7 100%);
  box-shadow:0 4px 5px rgba(75,50,33,.12);
}
.preview-head.santa{
  top:-10px;
  width:72px;
  height:49px;
  transform:translateX(-50%) rotate(-5deg);
}
.preview-head.santa .ps-cap{
  position:absolute;
  left:17px;
  top:5px;
  width:40px;
  height:30px;
  border-radius:30px 20px 6px 6px;
  background:linear-gradient(145deg,#e84f41,#bd302c 80%);
  transform:rotate(-10deg) skewX(-7deg);
}
.preview-head.santa .ps-cap:after{
  content:"";
  position:absolute;
  right:-12px;
  top:-1px;
  width:20px;
  height:20px;
  border-radius:50%;
  background:#fffdf8;
}
.preview-head.santa .ps-brim{
  position:absolute;
  left:11px;
  bottom:4px;
  width:50px;
  height:14px;
  border-radius:12px;
  background:#fffdf8;
  box-shadow:0 2px 3px rgba(75,50,33,.1);
}
@keyframes santaHatPop{
  from{opacity:0;transform:translateX(-50%) translateY(8px) rotate(-5deg) scale(.72)}
  to{opacity:1;transform:translateX(-50%) translateY(0) rotate(-5deg) scale(1)}
}

/* Animations */
@keyframes robotIdle{0%,100%{transform:translateX(-50%) translateY(0) rotate(-1deg)}50%{transform:translateX(-50%) translateY(-7px) rotate(1deg)}}
@keyframes robotPatrol{0%{transform:translateX(calc(-50% - 67px)) rotate(-4deg)}50%{transform:translateX(calc(-50% + 67px)) rotate(4deg)}100%{transform:translateX(calc(-50% - 67px)) rotate(-4deg)}}
@keyframes robotCharge{0%,100%{transform:translateX(-50%) scale(1)}50%{transform:translateX(-50%) translateY(-4px) scale(1.04)}}
@keyframes robotLow{0%{transform:translateX(-50%) translateX(-2px)}50%{transform:translateX(-50%) translateX(2px)}100%{transform:translateX(-50%) translateX(-2px)}}
@keyframes robotCelebrate{0%,100%{transform:translateX(-50%) translateY(0)}50%{transform:translateX(-50%) translateY(-35px) rotate(-5deg)}75%{transform:translateX(-50%) translateY(-7px) rotate(5deg)}}
@keyframes robotTap{0%,100%{transform:translateX(-50%) scale(1)}45%{transform:translateX(-50%) scale(.92,1.08)}70%{transform:translateX(-50%) scale(1.08,.94)}}
@keyframes blink{0%,45%,49%,100%{transform:scaleY(1)}47%{transform:scaleY(.08)}}
@keyframes sparkle{0%,100%{transform:scale(.85) rotate(-10deg);opacity:.55}50%{transform:scale(1.18) rotate(8deg);opacity:1}}
@keyframes ringSpin{from{transform:translateX(-50%) rotate(0)}to{transform:translateX(-50%) rotate(360deg)}}
@keyframes dustRise{0%{transform:translateY(0) scale(.6);opacity:0}25%{opacity:.65}100%{transform:translateY(-45px) translateX(15px) scale(1.25);opacity:0}}
@keyframes effectFly{0%{transform:translate(0,0) scale(.7);opacity:0}20%{opacity:1}100%{transform:translate(var(--move-x),-125px) scale(1.35) rotate(var(--rotate));opacity:0}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes popup{from{opacity:0;transform:scale(.88)}to{opacity:1;transform:scale(1)}}
@media(max-width:440px){body{padding:0}.phone{width:100%;height:100vh;border:0;border-radius:0}.notch{display:none}}


/* ===== Sticky robot room: only the lower control panel scrolls ===== */
#homePage.page{
  display:none;
  height:100%;
  padding:0;
  overflow:hidden;
  background:linear-gradient(180deg,#cfaa7d 0%,#e0c39a 39%,#d29c58 40%,#d09850 100%);
}
#homePage.page.active{
  display:flex;
  flex-direction:column;
}
#homePage .room{
  flex:0 0 355px;
  height:355px;
  min-height:355px;
  position:relative;
  z-index:12;
  overflow:hidden;
  box-shadow:0 8px 18px rgba(87,54,25,.14);
}
#homePage .home-dashboard{
  flex:1 1 auto;
  min-height:0;
  overflow-y:auto;
  -webkit-overflow-scrolling:touch;
  padding:10px 8px 24px;
  background:linear-gradient(180deg,rgba(239,205,151,.99),rgba(227,181,110,.99));
  border-top:2px solid rgba(120,76,38,.10);
}
#homePage .home-dashboard::-webkit-scrollbar{width:0;height:0}
#homePage .home-dashboard{scrollbar-width:none;}
@media(max-height:820px){
  #homePage .room{flex-basis:330px;height:330px;min-height:330px;}
}


/* ===== Balanced readable mode: keep original phone shape, enlarge text without stretching layout ===== */
.phone{
  width:min(100%,420px)!important;
  height:960px!important;
  border:8px solid #242321!important;
  border-radius:40px!important;
  overflow:hidden!important;
}
.notch{display:block!important;}
.header{
  height:136px!important;
  padding:24px 14px 8px!important;
}
.pages{height:calc(100% - 136px)!important;}
body{
  padding:8px!important;
  align-items:flex-start!important;
}
body,button,input,select{
  font-size:13px!important;
  word-break:keep-all;
}
.brand{font-size:11px!important;letter-spacing:1.2px!important;}
.app-title{font-size:29px!important;line-height:1.08!important;}
.coin-pill{font-size:14px!important;padding:9px 13px!important;}
.nav{margin-top:11px!important;gap:6px!important;}
.nav-btn{font-size:11px!important;min-height:36px!important;padding:8px 2px!important;border-radius:16px!important;}
.section-kicker{font-size:11px!important;}
.section-title{font-size:24px!important;}
#homePage .room{
  flex:0 0 330px!important;
  height:330px!important;
  min-height:330px!important;
}
#homePage .home-dashboard{
  padding:10px 8px 24px!important;
}
.speech{width:218px!important;min-height:86px!important;font-size:14px!important;line-height:1.55!important;padding:15px 14px!important;}
.speech strong{font-size:17px!important;}
.mode-chip{font-size:11px!important;padding:8px 14px!important;top:111px!important;}
.mission{width:98px!important;padding:9px 8px!important;}
.mission-title{font-size:12px!important;}
.mission-text{font-size:11px!important;line-height:1.45!important;}
.reward-small{font-size:11px!important;}
.quick{right:7px!important;top:86px!important;gap:7px!important;}
.quick-btn{width:54px!important;min-height:53px!important;font-size:10px!important;line-height:1.2!important;}
.quick-btn .icon{font-size:22px!important;}
.actions{gap:4px!important;padding:8px 5px!important;}
.action-btn{font-size:10px!important;line-height:1.15!important;}
.action-icon{font-size:23px!important;}
.plan-panel{padding:12px 10px!important;border-radius:16px!important;}
.plan-head{margin-bottom:8px!important;gap:8px!important;}
.plan-title{font-size:14px!important;line-height:1.25!important;}
.plan-model{font-size:11px!important;padding:5px 8px!important;white-space:nowrap!important;flex:0 0 auto!important;}
.learn-panel{padding:12px 10px!important;border-radius:15px!important;}
.learn-top{align-items:flex-start!important;gap:8px!important;}
.learn-title{font-size:14px!important;line-height:1.3!important;flex:1 1 auto!important;min-width:0!important;}
.learn-pill{
  font-size:11px!important;
  line-height:1.15!important;
  padding:6px 8px!important;
  white-space:nowrap!important;
  word-break:keep-all!important;
  flex:0 0 auto!important;
  min-width:58px!important;
  text-align:center!important;
}
.learn-desc{font-size:12px!important;line-height:1.55!important;}
.learn-status{font-size:12px!important;line-height:1.5!important;}
.learn-step{font-size:11px!important;line-height:1.25!important;padding:7px 5px!important;word-break:keep-all!important;}
.learn-btn{font-size:14px!important;min-height:45px!important;border-radius:13px!important;}
.condition-panel{padding:12px 10px!important;border-radius:15px!important;}
.condition-title{font-size:13px!important;line-height:1.45!important;margin-bottom:9px!important;}
.condition-row,.predict-condition-grid{
  grid-template-columns:76px 1fr 76px 1fr!important;
  gap:8px!important;
  align-items:center!important;
}
.condition-row label,.predict-condition-grid label{
  font-size:12px!important;
  white-space:nowrap!important;
  line-height:1.2!important;
}
.condition-select{font-size:13px!important;min-height:42px!important;padding:0 9px!important;border-radius:11px!important;}
.condition-help{font-size:12px!important;line-height:1.5!important;margin:8px 0 0!important;}
.profile-chip{display:inline-block;background:#edf8df;color:#2f8b3a;border:1px solid #d5ecc3;border-radius:999px;padding:5px 8px!important;font-size:11px!important;font-weight:900;margin-left:4px;white-space:nowrap!important;}
.first-learn-note{font-size:12px!important;line-height:1.55!important;padding:9px 10px!important;}
.predict-btn{font-size:14px!important;min-height:44px!important;border-radius:13px!important;}
.predict-loading{font-size:12px!important;line-height:1.5!important;min-height:24px!important;border-radius:10px;padding:6px 8px;background:rgba(255,255,255,.35);}
.predict-loading.active{background:#eaf4df;color:#2f8b3a;}
.scope-buttons{grid-template-columns:1.05fr repeat(5,1fr)!important;gap:5px!important;}
.scope-btn{font-size:10.5px!important;min-height:42px!important;padding:6px 3px!important;line-height:1.2!important;}
.selected-plan{grid-template-columns:1fr .82fr!important;gap:8px!important;}
.plan-summary{font-size:12px!important;line-height:1.35!important;padding:11px!important;}
.plan-soc{padding:11px 8px!important;}
.plan-soc-label{font-size:11px!important;}
.plan-soc-value{font-size:30px!important;}
.plan-soc-sub{font-size:11px!important;line-height:1.45!important;white-space:normal!important;}
.start-clean-primary{font-size:15px!important;min-height:54px!important;border-radius:15px!important;}
.start-clean-primary small{font-size:11px!important;}
.home-cards{grid-template-columns:1.1fr 1fr .78fr!important;gap:7px!important;}
.mini-card{padding:11px 9px!important;}
.mini-title{font-size:13px!important;}
.battery-info{font-size:11.5px!important;line-height:1.55!important;}
.battery-message{font-size:11px!important;line-height:1.45!important;}
.time-number{font-size:35px!important;}
.time-number small{font-size:14px!important;}
.time-sub{font-size:10.5px!important;}
.time-tip{font-size:11px!important;line-height:1.45!important;}
.food-title,.food-count{font-size:11.5px!important;}
.panel-title{font-size:16px!important;}
.badge{font-size:11px!important;}
.event-content strong{font-size:12.5px!important;}
.event-content span{font-size:11.5px!important;line-height:1.5!important;}
.event-time{font-size:11.5px!important;}
.reward-title{font-size:13px!important;}
.reward-desc{font-size:11.5px!important;line-height:1.5!important;}
.reward-btn{font-size:12px!important;}
.level-number{font-size:30px!important;}
.level-caption{font-size:11px!important;}
.modal{align-items:flex-end!important;justify-content:center!important;padding:0 16px 18px!important;background:rgba(45,33,23,.32)!important;backdrop-filter:blur(2px)!important;}
.modal-card{max-width:392px!important;padding:22px!important;border-radius:24px 24px 20px 20px!important;animation:sheetUp .22s ease-out!important;}
@keyframes sheetUp{from{opacity:0;transform:translateY(46px)}to{opacity:1;transform:translateY(0)}}
.modal-title{font-size:22px!important;}
.modal-body{font-size:15px!important;line-height:1.7!important;}
.modal-btn{font-size:15px!important;padding:13px!important;}
.toast{font-size:13px!important;line-height:1.5!important;min-width:260px;text-align:center;}
@media(max-width:440px){
  body{padding:8px!important;}
  .phone{
    width:min(calc(100% - 16px),420px)!important;
    height:960px!important;
    border:8px solid #242321!important;
    border-radius:40px!important;
  }
  .notch{display:block!important;}
  .header{height:136px!important;}
  .pages{height:calc(100% - 136px)!important;}
  .condition-row,.predict-condition-grid{grid-template-columns:72px 1fr 72px 1fr!important;gap:7px!important;}
  .condition-row label,.predict-condition-grid label{font-size:11.5px!important;}
  .condition-select{font-size:12.5px!important;padding:0 7px!important;}
}
@media(max-height:820px){
  #homePage .room{flex-basis:315px!important;height:315px!important;min-height:315px!important;}
  .speech{top:12px!important;}
}

/* CTA click safety: keep the first-learning button above decorative layers */
#learnPanel{position:relative!important;z-index:60!important;}
#learnBtn{position:relative!important;z-index:9999!important;pointer-events:auto!important;touch-action:manipulation!important;isolation:isolate!important;}
.learn-panel,.plan-panel,.home-dashboard{position:relative!important;}
.learn-panel{z-index:80!important;}
.condition-panel{position:relative!important;z-index:10!important;}

/* ===== Compact learning/profile summary cards ===== */
.compact-note{padding:9px 10px!important;line-height:1.35!important;}
.note-title{font-size:12px;font-weight:950;color:#6f4f38;margin-bottom:7px;}
.profile-mini-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:4px 0 7px;}
.profile-mini-grid span{display:flex;align-items:center;justify-content:center;min-height:28px;border-radius:9px;background:rgba(255,255,255,.72);font-size:11px;font-weight:950;color:#6f4f38;white-space:nowrap;}
.note-caption{font-size:11px;font-weight:850;color:#8a6a45;line-height:1.35;}
.summary-card{display:flex;flex-direction:column;gap:6px;}
.summary-title{font-size:12px;font-weight:950;color:#2f8b3a;margin-bottom:1px;}
.summary-row{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:5px 0;border-bottom:1px dashed rgba(124,83,43,.16);}
.summary-row:last-child{border-bottom:0;}
.summary-key{color:#7c5c3d;font-size:11px;font-weight:900;white-space:nowrap;}
.summary-val{color:#4b3324;font-size:11px;font-weight:950;text-align:right;line-height:1.25;}
.summary-val.em{color:#ef573f;font-size:15px;}
.summary-val.green{color:#2f8b3a;}

/* ===== User guidance banner: persistent next-step explanation ===== */
.flow-guide{
  margin:9px 0 8px;
  padding:10px 11px;
  border:1px solid rgba(78,139,58,.20);
  border-left:5px solid #62aa49;
  border-radius:13px;
  background:linear-gradient(145deg,#f3fbeb,#fff7dc);
  box-shadow:0 4px 10px rgba(79,48,21,.08);
  color:#4b3324;
  font-size:12px;
  line-height:1.5;
  font-weight:850;
}
.flow-guide b{font-weight:1000;color:#2f8b3a;}
.flow-guide .guide-step{display:block;margin-bottom:3px;color:#7a5a3c;font-size:11px;font-weight:1000;}
.flow-guide.warning{border-left-color:#ef8c32;background:linear-gradient(145deg,#fff5dc,#fff0cb);}
.flow-guide.warning b{color:#ef8c32;}
.flow-guide.danger{border-left-color:#ef4e45;background:linear-gradient(145deg,#fff0e9,#fff7dc);}
.flow-guide.danger b{color:#ef4e45;}
.flow-guide.done{border-left-color:#2f8b3a;background:linear-gradient(145deg,#eff9e8,#fff7dc);}
.flow-guide.charging{border-left-color:#f2a84d;background:linear-gradient(145deg,#fff2d2,#fff8e8);}

/* ===== Reward closet: equipped items stay on Home Genie ===== */
.robot-accessory{
  position:absolute;
  z-index:34;
  left:50%;
  transform:translateX(-50%);
  pointer-events:none;
  display:none;
  filter:drop-shadow(0 4px 4px rgba(64,38,18,.22));
}
.robot.has-custom-head .crown{display:none!important;}
.robot-head-deco{
  top:-38px;
  min-width:104px;
  height:62px;
  display:none;
  align-items:center;
  justify-content:center;
  text-align:center;
  font-size:43px;
  line-height:1;
}
.robot-head-deco.show{display:flex;animation:decoPop .34s ease-out;}
.robot-head-deco.ribbon{top:-35px;font-size:48px;}
/* 모자는 홈지니 머리 위에 실제로 얹힌 느낌이 나도록 낮게 배치 */
.robot-head-deco.hat{
  top:-38px;
  font-size:66px;
  height:58px;
  transform:translateX(-58%) rotate(-10deg);
  filter:drop-shadow(0 4px 4px rgba(64,38,18,.18));
}
/* 토끼/고양이는 동물 이모지가 아니라 홈지니 자체에 귀가 붙는 장착형 레이어 */
.robot-head-deco.ears{top:-42px;width:138px;height:78px;min-width:138px;}
.robot-head-deco.ears.show{display:block;animation:decoPop .34s ease-out;}
.robo-ear{position:absolute;z-index:2;bottom:4px;filter:drop-shadow(0 3px 3px rgba(64,38,18,.16));}
.robot-head-deco.bunny .robo-ear{
  width:22px;height:62px;border:3px solid #fff;border-radius:16px 16px 12px 12px;
  background:linear-gradient(180deg,#fff 0%,#f1edf8 100%);
}
.robot-head-deco.bunny .robo-ear:after{
  content:"";position:absolute;left:50%;top:8px;width:9px;height:43px;transform:translateX(-50%);
  border-radius:12px;background:linear-gradient(180deg,#ffb5ce,#ffd7e5);
}
.robot-head-deco.bunny .robo-ear.left{left:36px;transform:rotate(-8deg);transform-origin:bottom center;}
.robot-head-deco.bunny .robo-ear.right{right:36px;transform:rotate(8deg);transform-origin:bottom center;}
.robot-head-deco.cat .robo-ear{
  width:36px;
  height:34px;
  bottom:6px;
  background:linear-gradient(180deg,#ffbd4a 0%,#ff922e 82%,#f07725 100%);
  clip-path:polygon(50% 0,4% 100%,96% 100%);
  border-radius:8px;
  filter:drop-shadow(0 3px 3px rgba(64,38,18,.22));
}
.robot-head-deco.cat .robo-ear:after{
  content:"";
  position:absolute;
  left:50%;
  bottom:6px;
  width:16px;
  height:16px;
  transform:translateX(-50%);
  background:linear-gradient(180deg,#ffd6a7,#ff8f80);
  clip-path:polygon(50% 0,8% 100%,92% 100%);
}
.robot-head-deco.cat .robo-ear.left{left:20px;transform:rotate(-16deg);transform-origin:bottom center;}
.robot-head-deco.cat .robo-ear.right{right:20px;transform:rotate(16deg);transform-origin:bottom center;}
.robot-aura-deco{
  position:absolute;
  z-index:5;
  inset:-42px -46px -22px -46px;
  pointer-events:none;
  display:none;
}
.robot-aura-deco.show{display:block;}
.robot-aura-deco span{
  position:absolute;
  font-size:22px;
  filter:drop-shadow(0 3px 3px rgba(64,38,18,.18));
  animation:decoTwinkle 1.6s ease-in-out infinite;
}
.robot-aura-deco span:nth-child(1){left:7px;top:35px;animation-delay:.1s;}
.robot-aura-deco span:nth-child(2){right:2px;top:22px;animation-delay:.45s;}
.robot-aura-deco span:nth-child(3){right:18px;bottom:22px;animation-delay:.8s;}
.robot-aura-deco span:nth-child(4){left:22px;bottom:10px;animation-delay:1.05s;}
.level-robot-preview{position:relative;display:flex;align-items:center;justify-content:center;width:100%;min-width:0;min-height:120px;margin:0 auto 6px;}
.preview-shell{position:relative;width:122px;height:102px;display:grid;place-items:end center;margin:0 auto;}
.preview-crown,.preview-head,.preview-aura{position:absolute;pointer-events:none;}
.preview-crown{left:50%;top:-6px;transform:translateX(-50%);font-size:35px;line-height:1;filter:drop-shadow(0 3px 3px rgba(64,38,18,.18));}
.preview-robot{
  position:absolute;left:50%;bottom:8px;width:98px;height:54px;transform:translateX(-50%);
  border:2px solid #a29b92;border-radius:58% 58% 39% 39%;
  background:linear-gradient(180deg,#fffefb 0%,#e7e8e3 70%,#c5c7c1 100%);
  box-shadow:0 8px 12px rgba(55,37,21,.18),inset 0 -5px 8px rgba(83,83,79,.10);
  animation:float 2s ease-in-out infinite;
}
.preview-robot-top{
  position:absolute;left:50%;top:-4px;width:68px;height:31px;transform:translateX(-50%);
  border-top:2px solid rgba(119,119,114,.42);border-radius:50%;
  background:radial-gradient(ellipse at center,#fbfbf8 0%,#d5d6d2 74%,#b8b9b3 100%);
}
.preview-robot-face{
  position:absolute;z-index:3;left:50%;bottom:5px;width:69px;height:29px;transform:translateX(-50%);
  border-radius:15px 15px 17px 17px;background:linear-gradient(180deg,#2a2c2d,#101213 76%);
  box-shadow:inset 0 3px 4px rgba(255,255,255,.12);
}
.preview-eye{
  position:absolute;top:8px;width:11px;height:11px;border:1.6px solid #f2f0dc;border-radius:50%;background:#111;
}
.preview-eye:after{content:"";position:absolute;top:2px;left:3px;width:3.5px;height:3.5px;border-radius:50%;background:#fff;}
.preview-eye.left{left:11px}.preview-eye.right{right:11px}
.preview-cheek{position:absolute;bottom:4px;width:7px;height:3px;border-radius:50%;background:#ff8d8d;opacity:.78;}
.preview-cheek.left{left:5px}.preview-cheek.right{right:5px}
.preview-mouth{position:absolute;left:50%;bottom:4px;width:12px;height:6px;transform:translateX(-50%);border:1.6px solid #f3d6c9;border-top:0;border-radius:0 0 8px 8px;}
.preview-slot{position:absolute;left:50%;bottom:-1px;width:24px;height:3px;transform:translateX(-50%);border-radius:10px;background:#484a48;}
.preview-head{top:3px;left:50%;transform:translateX(-50%);font-size:31px;line-height:1;filter:drop-shadow(0 3px 3px rgba(64,38,18,.18));}
.preview-head.ribbon{top:1px;font-size:33px;}
.preview-head.hat{top:-3px;transform:translateX(-56%) rotate(-10deg);font-size:43px;}
.preview-head.ears{top:-8px;width:92px;height:48px;}
.preview-head.ears .p-ear{position:absolute;bottom:0;filter:drop-shadow(0 2px 2px rgba(64,38,18,.14));}
.preview-head.bunny .p-ear{width:13px;height:42px;border:2px solid #fff;border-radius:12px;background:#f5f1fb;}
.preview-head.bunny .p-ear:after{content:"";position:absolute;left:50%;top:6px;width:5px;height:29px;transform:translateX(-50%);border-radius:8px;background:#ffc2d7;}
.preview-head.bunny .p-ear.left{left:24px;transform:rotate(-8deg)}.preview-head.bunny .p-ear.right{right:24px;transform:rotate(8deg)}
.preview-head.cat .p-ear{width:24px;height:22px;background:linear-gradient(180deg,#ffbd4a,#ff922e 85%);clip-path:polygon(50% 0,4% 100%,96% 100%);}
.preview-head.cat .p-ear:after{content:"";position:absolute;left:50%;bottom:3px;width:10px;height:10px;transform:translateX(-50%);background:linear-gradient(180deg,#ffd6a7,#ff8f80);clip-path:polygon(50% 0,8% 100%,92% 100%);}
.preview-head.cat .p-ear.left{left:13px;transform:rotate(-15deg)}.preview-head.cat .p-ear.right{right:13px;transform:rotate(15deg)}
.preview-aura{inset:0;font-size:18px;animation:decoTwinkle 1.5s ease-in-out infinite;}
.preview-aura .a1{position:absolute;left:0;top:16px}.preview-aura .a2{position:absolute;right:-2px;top:28px}.preview-aura .a3{position:absolute;right:10px;bottom:12px}
.reward-btn.equipped{background:linear-gradient(90deg,#4a9b42,#75b84e)!important;color:#fff!important;}
.reward-btn.owned{background:#fff2cf!important;color:#5c422f!important;border:1px solid rgba(124,83,43,.18)!important;}
.reward-card.owned{background:rgba(255,253,240,.98)!important;border-color:rgba(75,155,66,.22)!important;}
.reward-card.equipped{box-shadow:0 0 0 2px rgba(75,155,66,.2), var(--shadow)!important;}
.reward-status{margin-top:5px;color:#4a9b42;font-size:10px;font-weight:950;min-height:13px;}

.reward-folder-tabs{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:10px 0 9px;}
.reward-folder-btn{min-height:43px;border:1px solid rgba(124,83,43,.18);border-radius:14px;background:rgba(255,248,231,.9);color:#6f4f38;font-size:13px;font-weight:950;box-shadow:0 4px 10px rgba(79,48,21,.1);}
.reward-folder-btn.active{background:linear-gradient(90deg,#4a9b42,#75b84e);color:#fff;border-color:transparent;}
.reward-panel{display:block;}
.reward-panel.hidden{display:none;}
.coupon-card{min-height:178px;text-align:left;display:flex;flex-direction:column;align-items:stretch;}
.coupon-card .reward-icon{text-align:center;font-size:34px;line-height:1.05;}
.coupon-card .reward-title{text-align:center;line-height:1.25;min-height:32px;display:flex;align-items:center;justify-content:center;}
.coupon-card .reward-desc{font-size:10.5px;line-height:1.5;text-align:left;min-height:58px;}
.coupon-benefit{margin-top:7px;padding:7px 8px;border-radius:10px;background:#fff2cf;color:#6f4f38;font-size:10px;font-weight:900;line-height:1.35;text-align:left;min-height:42px;display:flex;align-items:center;}
.coupon-card .reward-status{min-height:15px;text-align:center;}
.coupon-card .reward-btn{margin-top:auto;min-height:42px;display:flex;align-items:center;justify-content:center;text-align:center;}
.coupon-card.owned{border-color:rgba(75,155,66,.24);background:rgba(255,253,240,.98);}
.reward-btn.need-coins{background:#efe0bc!important;color:#6f4f38!important;}
.reward-btn.need-coins:after{content:"";}

@keyframes decoPop{from{opacity:0;transform:translateX(-50%) translateY(8px) scale(.7)}to{opacity:1;transform:translateX(-50%) translateY(0) scale(1)}}
@keyframes decoTwinkle{0%,100%{opacity:.45;transform:scale(.88) rotate(-8deg)}50%{opacity:1;transform:scale(1.12) rotate(8deg)}}

/* ===== Room status cleanup: avoid speech overlap + show current robot 배터리 ===== */
#homePage .room .mode-chip{
  top:125px!important;
  left:12px!important;
  right:auto!important;
  bottom:auto!important;
  transform:none!important;
  width:142px!important;
  max-width:142px!important;
  min-height:34px!important;
  padding:7px 9px!important;
  border-radius:15px!important;
  background:rgba(255,248,229,.96)!important;
  box-shadow:0 5px 12px rgba(72,46,23,.18)!important;
  color:#5b3f2d!important;
  font-size:10.5px!important;
  line-height:1.25!important;
  font-weight:950!important;
  text-align:center!important;
  white-space:normal!important;
  word-break:keep-all!important;
}
#homePage .room.cleaning .mode-chip{color:#fff!important;background:rgba(57,143,82,.94)!important;}
#homePage .room.charging .mode-chip{color:#fff!important;background:rgba(242,145,35,.94)!important;}
.robot-soc-badge{
  position:absolute;
  z-index:24;
  right:64px;
  bottom:114px;
  width:98px;
  min-height:44px;
  padding:7px 8px 6px;
  border:2px solid rgba(255,255,255,.82);
  border-radius:16px;
  background:rgba(255,255,255,.95);
  box-shadow:0 7px 16px rgba(60,38,20,.22);
  text-align:center;
  pointer-events:auto;
}
.robot-soc-badge span{
  display:block;
  color:#7a5a3c;
  font-size:9.5px;
  line-height:1.05;
  font-weight:950;
  white-space:nowrap;
}
.robot-soc-badge b{
  display:block;
  margin-top:2px;
  color:#2f8b3a;
  font-size:19px;
  line-height:1;
  font-weight:1000;
  letter-spacing:-.5px;
}
.battery-help-btn{
  position:absolute;
  top:-7px;
  right:-7px;
  z-index:3;
  width:19px;
  height:19px;
  padding:0;
  border:2px solid rgba(255,255,255,.96);
  border-radius:50%;
  background:linear-gradient(180deg,#8fcf71,#43a549);
  color:#fff;
  box-shadow:0 3px 8px rgba(54,38,20,.23);
  font-size:12px;
  line-height:15px;
  font-weight:1000;
  text-align:center;
  cursor:pointer;
}
.battery-help-btn:active{transform:scale(.94)}
.battery-help-btn:hover{filter:brightness(1.04)}
.robot-soc-badge.need b{color:#ef8c32;}
.robot-soc-badge.low b{color:#ef4e45;}
.robot-soc-badge.ok b{color:#2f8b3a;}
.robot-soc-badge:after{
  content:"";
  position:absolute;
  left:50%;
  bottom:-8px;
  transform:translateX(-50%);
  border-width:8px 6px 0;
  border-style:solid;
  border-color:rgba(255,255,255,.95) transparent transparent;
}
@media(max-height:820px){
  #homePage .room .mode-chip{top:118px!important;}
  .robot-soc-badge{right:60px;bottom:105px;}
}

/* ===== SVG learned home map card ===== */
.learn-steps.map-ready,
#learnSteps.map-ready{
  display:block!important;
  grid-template-columns:1fr!important;
  gap:0!important;
  width:100%!important;
}
#learnSteps.map-ready .home-map-card{
  width:100%!important;
  max-width:none!important;
}
.home-map-card{
  width:100%;
  padding:6px;
  margin-top:8px;
  border-radius:16px;
  background:rgba(255,255,255,.72);
  border:1px solid rgba(124,83,43,.14);
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.48);
}
.home-map-head{
  display:flex;
  align-items:center;
  justify-content:flex-end;
  gap:8px;
  margin-bottom:5px;
}
.home-map-title{display:none;}
.home-map-badge{
  flex:0 0 auto;
  padding:4px 8px;
  border-radius:999px;
  background:#e8f5dc;
  color:#2f8b3a;
  font-size:10px;
  line-height:1;
  font-weight:950;
  white-space:nowrap;
}
.home-map-img-wrap{
  position:relative;
  overflow:hidden;
  width:100%;
  min-height:210px;
  border-radius:14px;
  background:linear-gradient(145deg,#f6e3ba,#fff7e4);
  border:1px solid rgba(124,83,43,.12);
}
.home-map-svg{display:block;width:100%;height:220px;}
.home-map-caption{display:none;}
.map-room{stroke:#fffdf4;stroke-width:4;filter:drop-shadow(0 3px 4px rgba(67,42,20,.13));}
.map-room.dashed{stroke-dasharray:8 5;stroke:#fffdf4;}
.map-room-label{fill:#64472f;font-size:13px;font-weight:950;text-anchor:middle;dominant-baseline:middle;}
.map-room-sub{fill:#8a6744;font-size:9.4px;font-weight:850;text-anchor:middle;dominant-baseline:middle;}
.map-route{fill:none;stroke:rgba(255,255,255,.82);stroke-width:3;stroke-linecap:round;stroke-dasharray:5 6;}
.map-room-group{cursor:pointer;}
.map-room-group .map-room{transition:opacity .18s ease, filter .18s ease;}
.map-room-group.no-go .map-room{opacity:.42;filter:grayscale(.35);}
.map-no-go-shade{fill:rgba(255,255,255,.48);}
.map-no-go-line{stroke:#8b6f57;stroke-width:4;stroke-linecap:round;opacity:.72;}
.map-action-row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:7px;margin-top:8px;}
.map-action-btn{
  min-height:38px;
  border:0;
  border-radius:13px;
  background:#fff4d8;
  color:#68472d;
  font-size:11.5px;
  font-weight:950;
  box-shadow:inset 0 0 0 1px rgba(135,88,43,.16);
  cursor:pointer;
}
.map-action-btn.active{color:#fff;background:linear-gradient(135deg,#50ae48,#77c75b);box-shadow:0 7px 12px rgba(67,126,56,.20);}
.map-action-btn.danger.active{background:linear-gradient(135deg,#f07a54,#f7a13e);box-shadow:0 7px 12px rgba(190,93,45,.20);}
/* 매핑 완료 후 지도 바로 아래에서 즉시 실행할 수 있는 메인 CTA */
.map-clean-now-btn{
  position:relative;
  z-index:30;
  width:100%;
  min-height:48px;
  margin-top:8px;
  padding:9px 12px;
  border:0;
  border-radius:14px;
  background:linear-gradient(90deg,#ef8c32,#ffad45);
  color:#fff;
  font-size:14px;
  line-height:1.25;
  font-weight:800;
  box-shadow:0 7px 14px rgba(215,116,36,.24);
  cursor:pointer;
  touch-action:manipulation;
}
.map-clean-now-btn:active{transform:scale(.985);}
.map-clean-now-btn:disabled{
  opacity:.58;
  filter:grayscale(.08);
  cursor:not-allowed;
  box-shadow:none;
}
.map-clean-now-btn .map-clean-sub{
  display:block;
  margin-top:2px;
  color:rgba(255,255,255,.90);
  font-size:10px;
  line-height:1.25;
  font-weight:500;
}
.map-action-hint{
  margin-top:7px;
  padding:7px 9px;
  border-radius:12px;
  background:rgba(255,250,235,.92);
  border:1px solid rgba(124,83,43,.10);
  color:#6f4f36;
  font-size:11px;
  line-height:1.38;
  font-weight:850;
  text-align:center;
}
.map-action-hint b{color:#2f8b3a;}
.map-legend{
  display:flex;
  align-items:center;
  justify-content:center;
  flex-wrap:wrap;
  gap:7px 10px;
  margin-top:8px;
  padding:8px 8px;
  border-radius:14px;
  background:rgba(255,250,235,.92);
  border:1px solid rgba(124,83,43,.13);
  color:#68472d;
  font-size:12px;
  line-height:1.15;
  font-weight:950;
}
.map-legend-title{color:#4b3324;font-weight:1000;margin-right:2px;}
.map-legend-item{display:inline-flex;align-items:center;gap:5px;}
.map-dot{display:inline-block;width:12px;height:12px;border-radius:999px;border:1px solid rgba(80,50,28,.16);box-shadow:0 1px 2px rgba(72,43,19,.12);}
.dot-clean{background:#cfeec0;}
.dot-normal{background:#ffe08a;}
.dot-dusty{background:#ffb169;}
.dot-focus{background:#ff7d68;}

/* ===== Main map CTA row ===== */
.learn-actions{display:grid;grid-template-columns:1fr;gap:8px;margin-top:8px;}
.learn-actions.ready{grid-template-columns:1fr 1fr;}
.clean-execute-btn{
  position:relative;
  z-index:9999;
  width:100%;
  min-height:45px;
  border:0;
  border-radius:13px;
  background:linear-gradient(90deg,#41a346,#79c75a);
  color:#fff;
  font-size:14px;
  font-weight:950;
  box-shadow:0 7px 12px rgba(67,126,56,.22);
  cursor:pointer;
  pointer-events:auto!important;
  touch-action:manipulation!important;
}
.clean-execute-btn:disabled{opacity:.55;cursor:not-allowed;filter:grayscale(.12);}
.condition-panel.manual-mode{margin-top:9px!important;background:linear-gradient(145deg,#fff8e6,#f3dfb2)!important;}
.condition-panel.manual-mode .condition-title:before{content:"✍️ ";}

/* ===== Home simplification: one main clean-prep button, no extra lower cards ===== */
.scope-buttons,
.selected-plan,
.start-clean-primary,
.actions,
.home-cards{display:none!important;}
.condition-panel{margin-bottom:0!important;}
.predict-btn{position:relative;z-index:30;}
#flowGuide{margin-top:9px;}

.manual-action-row{
  display:grid;
  grid-template-columns:1fr 1fr;
  gap:8px;
  margin-top:10px;
}
.manual-clean-btn{
  position:relative;
  z-index:31;
  width:100%;
  min-height:43px;
  border:0;
  border-radius:13px;
  color:#fff;
  background:linear-gradient(90deg,#f69028,#f9b047);
  font-size:12.5px;
  font-weight:950;
  box-shadow:0 7px 12px rgba(210,117,35,.18);
  cursor:pointer;
}
.manual-clean-btn.ready{
  background:linear-gradient(90deg,#41a346,#79c75a);
  box-shadow:0 7px 12px rgba(67,126,56,.20);
}
.manual-clean-btn:disabled{
  opacity:.55;
  cursor:not-allowed;
  filter:grayscale(.12);
}
.manual-action-row .predict-btn{
  margin-top:0!important;
}
.manual-combo-btn{
  width:100%;
  min-height:46px!important;
  margin-top:10px!important;
  border-radius:14px!important;
  font-size:13px!important;
  font-weight:950!important;
  background:linear-gradient(90deg,#41a346,#79c75a)!important;
  color:#fff!important;
  box-shadow:0 7px 12px rgba(67,126,56,.22)!important;
}
.manual-combo-btn.running{
  background:linear-gradient(90deg,#f69028,#f9b047)!important;
}

/* ===== Home WOW features: station motion, route, map progress, prep cards ===== */
.room:after{
  content:"";
  position:absolute;
  z-index:6;
  left:92px;
  bottom:92px;
  width:54px;
  height:15px;
  border-radius:999px;
  background:rgba(64,42,26,.18);
  opacity:0;
  transform:scale(.7);
  transition:.25s ease;
}
.room.returning:after,
.room.docked:after{
  opacity:1;
  transform:scale(1);
}
.room.returning .robot{
  animation:robotReturnStation .95s ease-in-out forwards!important;
}
.room.docked .robot,
.room.charging .robot{
  animation:robotDockBreath 1.15s ease-in-out infinite!important;
  transform:translateX(calc(-50% - 105px)) translateY(-38px) scale(.72)!important;
}
.room.departing .robot{
  animation:robotDepartStation .85s ease-in-out forwards!important;
}
.room.charging .charge-ring,
.room.docked .charge-ring{
  left:104px!important;
  bottom:69px!important;
  width:118px!important;
  height:74px!important;
  opacity:.92!important;
  animation:ringSpin 1.05s linear infinite!important;
}
.room.cleaning .clean-path,
.room.route-preview .clean-path{
  opacity:1;
}
.room.route-preview .clean-fill{
  width:64%!important;
  animation:pathPreviewPulse 1.7s ease-in-out infinite;
}
.room.docked .clean-path,
.room.returning .clean-path{
  opacity:.28;
}
.map-room-group{cursor:pointer;}
.map-room-group .map-room{
  transition:opacity .18s ease, filter .18s ease, stroke-width .18s ease;
}
.map-room-group.planned .map-room{
  stroke:#36b04a;
  stroke-width:5.2;
  filter:drop-shadow(0 0 3px rgba(54,176,74,.35));
  animation:plannedGreenBlink 1.15s ease-in-out infinite;
}
.map-room-group.dirty-selected .map-room{
  stroke:#36b04a;
  stroke-width:5.2;
  filter:drop-shadow(0 0 3px rgba(54,176,74,.35));
  animation:plannedGreenBlink 1.05s ease-in-out infinite;
}
.map-dirty-ring,
.map-dirty-spark{
  display:none!important;
}
.map-room-group.dimmed .map-room{
  opacity:.28;
  filter:grayscale(.35);
}
.map-room-group.cleaning-zone .map-room{
  animation:plannedGreenBlink .9s ease-in-out infinite;
  stroke:#27a844;
  stroke-width:6.2;
}
.map-room-group.completed .map-room{
  opacity:.62;
}
.map-room-group.no-go .map-room{
  opacity:.40;
  filter:grayscale(.42);
}
.map-no-go-shade{fill:rgba(255,255,255,.52);}
.map-no-go-line{stroke:#6b5543;stroke-width:4.5;stroke-linecap:round;opacity:.78;}
.map-check{
  fill:#2f8b3a;
  font-size:14px;
  font-weight:950;
  text-anchor:middle;
  dominant-baseline:middle;
}
.map-route,
.map-route.active-route{
  opacity:0!important;
  display:none!important;
}
.map-action-hint.status-ready{
  border-color:rgba(73,163,68,.22);
  background:#f3ffe9;
}
.map-recommend-card{
  display:flex;
  align-items:center;
  gap:7px;
  margin-top:7px;
  padding:8px 9px;
  border-radius:13px;
  background:linear-gradient(135deg,#fffaf0,#f9e5b9);
  border:1px solid rgba(124,83,43,.12);
  color:#60452f;
  font-size:11px;
  line-height:1.38;
  font-weight:900;
}
.map-recommend-card .rec-icon{
  flex:0 0 auto;
  display:grid;
  place-items:center;
  width:26px;
  height:26px;
  border-radius:50%;
  background:#fff4d8;
  box-shadow:inset 0 0 0 1px rgba(124,83,43,.13);
}
.map-prep-card{
  display:grid;
  grid-template-columns:1fr auto;
  gap:6px;
  align-items:center;
  margin-top:7px;
  padding:8px 10px;
  border-radius:13px;
  background:rgba(255,255,255,.74);
  border:1px solid rgba(124,83,43,.12);
}
.map-prep-title{
  color:#4b3324;
  font-size:11.5px;
  line-height:1.35;
  font-weight:950;
}
.map-prep-sub{
  margin-top:2px;
  color:#7b5a3e;
  font-size:10px;
  line-height:1.35;
  font-weight:850;
}
.map-prep-badge{
  padding:5px 8px;
  border-radius:999px;
  color:#fff;
  background:#ef8c32;
  font-size:10px;
  font-weight:950;
  white-space:nowrap;
}
@keyframes robotReturnStation{
  0%{transform:translateX(-50%) translateY(0) scale(1) rotate(0)}
  55%{transform:translateX(calc(-50% - 72px)) translateY(-14px) scale(.88) rotate(-4deg)}
  100%{transform:translateX(calc(-50% - 105px)) translateY(-38px) scale(.72) rotate(0)}
}
@keyframes robotDepartStation{
  0%{transform:translateX(calc(-50% - 105px)) translateY(-38px) scale(.72)}
  65%{transform:translateX(calc(-50% - 40px)) translateY(-12px) scale(.9) rotate(3deg)}
  100%{transform:translateX(-50%) translateY(0) scale(1)}
}
@keyframes robotDockBreath{
  0%,100%{transform:translateX(calc(-50% - 105px)) translateY(-38px) scale(.72)}
  50%{transform:translateX(calc(-50% - 105px)) translateY(-43px) scale(.75)}
}
@keyframes pathPreviewPulse{
  0%,100%{opacity:.55}
  50%{opacity:1}
}
@keyframes mapZonePulse{
  0%,100%{filter:drop-shadow(0 4px 6px rgba(55,164,71,.22))}
  50%{filter:drop-shadow(0 4px 10px rgba(55,164,71,.58))}
}
@keyframes routeDash{
  from{stroke-dashoffset:36}
  to{stroke-dashoffset:0}
}
@keyframes dirtyZoneGlow{
  0%,100%{filter:drop-shadow(0 0 3px rgba(255,216,77,.34))}
  50%{filter:drop-shadow(0 0 8px rgba(255,216,77,.74))}
}
@keyframes dirtyRingDash{
  from{stroke-dashoffset:24}
  to{stroke-dashoffset:0}
}
@keyframes plannedGreenBlink{
  0%,100%{
    stroke:#36b04a;
    stroke-width:4.2;
    filter:drop-shadow(0 0 2px rgba(54,176,74,.25));
  }
  50%{
    stroke:#20c949;
    stroke-width:6.4;
    filter:drop-shadow(0 0 6px rgba(54,176,74,.55));
  }
}


/* ===== Map robot marker: 지도 위에서 홈지니가 실제로 움직이며 청소하는 표현 ===== */
.map-sweep{fill:none;stroke:rgba(255,255,255,.80);stroke-width:7;stroke-linecap:round;stroke-linejoin:round;pointer-events:none;}
.map-robot{pointer-events:none;}
.map-robot-shadow{fill:rgba(64,42,26,.22);}
.map-robot-shell{fill:#fbfbf8;stroke:#a29b92;stroke-width:1.4;}
.map-robot-face{fill:#1f2122;}
.map-robot-eye{fill:#fff;}
.map-robot-light{fill:#62aa49;animation:mapRobotBlink 1s ease-in-out infinite;}
.map-robot-body{animation:mapRobotBob .7s ease-in-out infinite;}
.map-robot-crown{font-size:7px;text-anchor:middle;}
.map-robot-puff{fill:rgba(255,255,255,.75);animation:mapPuff 1s ease-out infinite;}
.map-robot-puff.p2{animation-delay:.33s;}
.map-robot-puff.p3{animation-delay:.66s;}
@keyframes mapRobotBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-1.2px)}}
@keyframes mapRobotBlink{0%,100%{opacity:.45}50%{opacity:1}}
@keyframes mapPuff{0%{opacity:.8;transform:translate(0,0) scale(.5)}100%{opacity:0;transform:translate(-9px,-4px) scale(1.4)}}

/* ===== Top learning / clean action buttons alignment ===== */
.learn-actions.ready{
  grid-template-columns:1fr 1fr!important;
  align-items:stretch!important;
}
.learn-actions.ready .learn-btn,
.learn-actions.ready .clean-execute-btn{
  width:100%!important;
  height:48px!important;
  min-height:48px!important;
  padding:0 8px!important;
  border-radius:14px!important;
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  text-align:center!important;
  line-height:1.18!important;
  white-space:normal!important;
  word-break:keep-all!important;
  box-sizing:border-box!important;
  margin:0!important;
}
.learn-actions.ready .learn-btn{
  background:linear-gradient(90deg,#41a346,#79c75a)!important;
  color:#fff!important;
  font-size:12.5px!important;
  font-weight:950!important;
  box-shadow:0 7px 12px rgba(67,126,56,.20)!important;
}
.learn-actions.ready .clean-execute-btn{
  background:linear-gradient(90deg,#f69028,#f9b047)!important;
  color:#fff!important;
  font-size:13px!important;
  font-weight:950!important;
  box-shadow:0 7px 12px rgba(210,117,35,.22)!important;
}
.learn-actions.ready .clean-execute-btn:disabled{
  opacity:.62!important;
  filter:grayscale(.08)!important;
}


/* ============================================================
   NEW PAGE 2 · 부품 케어 (부품 상태 + 실시간 케어 기록)
   ============================================================ */
.parts-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.part-card{display:flex;align-items:center;gap:8px;padding:12px 10px;border:1px solid rgba(136,87,40,.14);border-radius:16px;background:rgba(255,248,231,.97);box-shadow:var(--shadow);cursor:pointer;text-align:left;}
.part-card:active{transform:scale(.98);}
.part-icon{flex:0 0 auto;width:44px;height:44px;display:grid;place-items:center;border-radius:14px;background:#f5eddb;font-size:25px;}
.part-info{flex:1 1 auto;min-width:0;}
.part-name{font-size:11.5px;font-weight:900;color:#7a5a3c;}
.part-status{margin-top:3px;font-size:12.5px;font-weight:950;line-height:1.3;word-break:keep-all;}
.part-face{flex:0 0 auto;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;font-size:17px;}
.part-card.good .part-status{color:#2f8b3a;}.part-card.good .part-face{background:#dff3cd;}
.part-card.check .part-status{color:#e07a1f;}.part-card.check .part-face{background:#ffe6c2;}
.part-card.bad .part-status{color:#ef4e45;}.part-card.bad .part-face{background:#ffd9d4;}
/* ===== Page 2 hero: user benefit first ===== */
.care-impact-hero{
  position:relative;
  overflow:hidden;
  margin-bottom:10px;
  padding:15px 14px 13px;
  border:1px solid rgba(71,145,60,.18);
  background:linear-gradient(145deg,#f5ffe9 0%,#fff7dc 58%,#ffe8b7 100%);
  box-shadow:0 10px 24px rgba(68,99,43,.15);
}
.care-impact-hero:before{
  content:"";
  position:absolute;
  right:-36px;
  top:-42px;
  width:126px;
  height:126px;
  border-radius:50%;
  background:rgba(255,255,255,.48);
}
.care-impact-top{position:relative;z-index:2;display:flex;align-items:flex-start;justify-content:space-between;gap:9px;}
.care-impact-eyebrow{color:#4a9b42;font-size:9px;font-weight:1000;letter-spacing:1px;}
.care-impact-title{margin-top:4px;color:#3f3025;font-size:17px;line-height:1.25;font-weight:1000;}
.care-impact-badge{
  flex:0 0 auto;
  padding:5px 8px;
  border-radius:999px;
  background:rgba(255,255,255,.78);
  color:#6f5940;
  border:1px solid rgba(124,83,43,.10);
  font-size:9px;
  line-height:1;
  font-weight:950;
  white-space:nowrap;
}
.care-impact-copy{position:relative;z-index:2;margin-top:8px;color:#6f543d;font-size:11.5px;line-height:1.5;font-weight:850;}
.care-impact-copy b{color:#2f8b3a;font-weight:1000;}
.care-impact-grid{position:relative;z-index:2;display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:11px;}
.care-impact-card{
  min-height:118px;
  padding:11px 9px 10px;
  border-radius:16px;
  background:rgba(255,255,255,.90);
  border:1px solid rgba(124,83,43,.09);
  box-shadow:0 6px 13px rgba(73,48,28,.09);
  text-align:center;
}
.care-impact-card.life{box-shadow:inset 0 4px 0 rgba(75,155,66,.65),0 6px 13px rgba(73,48,28,.09);}
.care-impact-card.money{box-shadow:inset 0 4px 0 rgba(239,140,50,.72),0 6px 13px rgba(73,48,28,.09);}
.care-impact-icon{font-size:25px;line-height:1;}
.care-impact-label{margin-top:6px;color:#76553e;font-size:10.5px;line-height:1.25;font-weight:950;}
.care-impact-value{display:flex;align-items:baseline;justify-content:center;gap:3px;margin-top:5px;color:#2f8b3a;}
.care-impact-card.money .care-impact-value{color:#ef7f2d;}
.care-impact-value strong{font-size:27px;line-height:1;font-weight:1000;letter-spacing:-.8px;}
.care-impact-value span{font-size:11px;font-weight:950;}
.care-impact-sub{margin-top:5px;color:#876a4d;font-size:9.5px;line-height:1.25;font-weight:900;}
.care-impact-foot{
  position:relative;
  z-index:2;
  display:flex;
  align-items:center;
  justify-content:center;
  margin-top:9px;
  padding:8px 9px;
  border-radius:12px;
  background:rgba(235,248,222,.92);
  color:#3a7f38;
  font-size:10.5px;
  line-height:1.4;
  font-weight:900;
  text-align:center;
}
.care-impact-foot b{font-weight:1000;color:#2f8b3a;}
.care-impact-disclaimer{margin-top:7px;color:#90765c;font-size:8.5px;line-height:1.4;font-weight:800;text-align:center;}
.care-subhead{display:flex;align-items:center;justify-content:space-between;margin:11px 2px 7px;color:#4b3324;font-size:13px;font-weight:1000;}
.care-subhead small{color:#8d7054;font-size:9.5px;font-weight:850;}

.care-summary{margin-top:9px;padding:14px;}
.care-lead{font-size:12px;line-height:1.55;font-weight:850;color:#6f4f38;}
.care-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:10px;}
.care-stat{padding:10px 6px;border-radius:13px;background:#fff2cf;text-align:center;}
.care-stat span{display:block;font-size:10.5px;font-weight:900;color:#7a5a3c;line-height:1.3;}
.care-stat b{display:block;margin-top:5px;color:#2f8b3a;font-size:22px;font-weight:1000;line-height:1;}
.care-stat small{font-size:10px;font-weight:900;color:#7a5a3c;}
.care-health-row{display:flex;align-items:center;gap:8px;margin-top:12px;font-size:11.5px;font-weight:900;}
.care-health-track{flex:1;height:10px;overflow:hidden;border-radius:10px;background:#ead9b9;}
.care-health-fill{height:100%;border-radius:inherit;background:linear-gradient(90deg,#62aa49,#ffd44f);transition:width .3s;}
.care-note{margin-top:10px;padding:9px 10px;border-radius:12px;background:#eaf4df;color:#2f8b3a;font-size:11.5px;line-height:1.5;font-weight:850;}
.event-tag{display:inline-block;margin-left:5px;padding:2px 7px;border-radius:999px;background:#eaf4df;color:#2f8b3a;font-size:9.5px!important;font-weight:950;vertical-align:middle;line-height:1.3;}
.modal-emoji{font-size:64px;text-align:center;padding:10px 0 14px;}
.modal-img{width:100%;max-height:300px;object-fit:cover;border-radius:14px;margin-bottom:10px;display:block;}


/* ===== Page 2 · Battery care simplified: current state first ===== */
.battery-care-main{
  margin-bottom:10px;
  padding:14px 13px 13px;
  background:linear-gradient(145deg,#fff8e8 0%,#fff1cc 100%);
  border:1px solid rgba(124,83,43,.12);
}
.battery-care-head{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;}
.battery-care-kicker{color:#4a9b42;font-size:9px;font-weight:800;letter-spacing:1px;}
.battery-care-title{margin-top:3px;color:#4b3324;font-size:18px;line-height:1.25;font-weight:800;}
.battery-care-badge{flex:0 0 auto;padding:6px 9px;border-radius:999px;background:#fff3cf;color:#7b5b3d;font-size:10px;font-weight:700;border:1px solid rgba(124,83,43,.10);}
.battery-care-copy{margin-top:9px;color:#6f543d;font-size:11.5px;line-height:1.6;font-weight:500;}
.battery-care-copy b{color:#2f8b3a;font-weight:700;}
.battery-health-card{margin-top:11px;padding:12px 11px;border-radius:15px;background:rgba(255,255,255,.86);border:1px solid rgba(124,83,43,.10);box-shadow:0 5px 12px rgba(73,48,28,.07);}
.battery-health-top{display:flex;align-items:flex-end;justify-content:space-between;gap:10px;}
.battery-health-label{color:#76553e;font-size:11px;font-weight:700;}
.battery-health-state{margin-top:3px;color:#2f8b3a;font-size:12px;font-weight:700;}
.battery-health-value{color:#2f8b3a;font-size:28px;line-height:1;font-weight:800;letter-spacing:-.8px;}
.battery-health-track{height:10px!important;margin-top:10px!important;}
.battery-care-stats{grid-template-columns:repeat(2,1fr)!important;margin-top:9px!important;}
.battery-care-stats .care-stat{min-height:72px;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:9px 5px;background:#fff2cf;}
.battery-care-stats .care-stat span{min-height:22px;display:flex;align-items:center;justify-content:center;font-size:10px;line-height:1.25;font-weight:700;}
.battery-life-guide{display:flex;align-items:center;gap:9px;margin-top:9px;padding:10px 11px;border:1px solid rgba(124,83,43,.10);border-radius:13px;background:rgba(255,255,255,.70);color:#60452f;}
.battery-life-guide-icon{flex:0 0 auto;width:31px;height:31px;display:grid;place-items:center;border-radius:10px;background:#fff2cf;font-size:18px;}
.battery-life-guide-copy{flex:1 1 auto;min-width:0;font-size:10.5px;line-height:1.45;font-weight:550;}
.battery-life-guide-copy b{display:block;margin-bottom:4px;color:#4b3324;font-size:11px;font-weight:750;}
.battery-life-usage-row{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin-bottom:3px;}
.battery-use-day{display:inline-flex;align-items:center;min-height:22px;padding:3px 7px;border-radius:999px;background:#eaf4df;color:#2f8b3a;font-size:10px;line-height:1;font-weight:800;white-space:nowrap;}
.battery-life-sub{color:#765b43;font-size:9.8px;line-height:1.4;font-weight:550;}
.battery-life-guide-btn{flex:0 0 auto;min-height:31px;padding:0 8px;border:1px solid rgba(74,155,66,.20);border-radius:10px;background:#eaf4df;color:#2f8b3a;font-size:9.5px;font-weight:750;white-space:nowrap;}
.battery-care-stats .care-stat b{font-size:22px;font-weight:800;}
.battery-care-stats .care-stat small{font-size:9.5px;font-weight:600;}
.battery-care-main .care-note{margin-top:9px;padding:9px 10px;border-radius:12px;background:#eaf4df;color:#2f8b3a;font-size:10.8px;line-height:1.5;font-weight:600;}
.care-subhead{margin-top:12px!important;}
.care-events-panel{margin-top:10px!important;}

/* ============================================================
   NEW PAGE 3 · 예약 청소 (출퇴근 맞춤 + 테마 기간 청소)
   ============================================================ */
.sched-panel{padding:14px;margin-bottom:9px;}
.sched-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px;}
.sched-title{font-size:15px;font-weight:950;}
.sched-desc{margin-top:4px;font-size:11.5px;line-height:1.5;font-weight:800;color:#76533b;}
.switch{flex:0 0 auto;position:relative;width:50px;height:28px;border:0;border-radius:999px;background:#d8c7a6;transition:.2s;}
.switch .knob{position:absolute;top:3px;left:3px;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 2px 5px rgba(0,0,0,.2);transition:.2s;}
.switch.on{background:#4a9b42;}.switch.on .knob{left:25px;}
.sched-body{margin-top:11px;}
.sched-body.off{opacity:.5;pointer-events:none;filter:grayscale(.2);}
.time-row{display:grid;grid-template-columns:38px 1fr 38px 1fr;gap:7px;align-items:center;}
.time-row label{font-size:12px;font-weight:900;color:#6c4a2f;}
.day-chips{display:grid;grid-template-columns:repeat(7,1fr);gap:5px;margin-top:9px;}
.day-chip{min-height:34px;border:1px solid rgba(124,83,43,.18);border-radius:11px;background:#f3e2be;color:#6f4f38;font-size:12px;font-weight:950;}
.day-chip.on{background:linear-gradient(180deg,#65ae4b,#368e3d);color:#fff;border-color:transparent;}
.sched-options{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-top:9px;}
.sched-opt{min-height:40px;border:1px solid rgba(124,83,43,.16);border-radius:12px;background:#fff4d5;color:#5a412e;font-size:11.5px;font-weight:950;line-height:1.25;padding:6px;}
.sched-opt.active{background:linear-gradient(90deg,#ef8c32,#ffb24b);color:#fff;border-color:transparent;}
.sched-preview{margin-top:10px;padding:10px 11px;border-radius:12px;background:#eaf4df;color:#2f8b3a;font-size:12px;line-height:1.6;font-weight:900;}
.sched-preview b{color:#ef573f;}
.sched-preview.off{background:#f3e2be;color:#7a5a3c;}
.sub-title{margin:14px 0 8px;font-size:15px;font-weight:950;}
.theme-list{display:flex;flex-direction:column;gap:8px;}
.theme-card{display:grid;grid-template-columns:46px 1fr auto;gap:10px;align-items:center;padding:12px;border:1px solid rgba(136,87,40,.14);border-radius:16px;background:rgba(255,248,231,.97);box-shadow:var(--shadow);}
.theme-card.on{border-color:rgba(75,155,66,.35);box-shadow:0 0 0 2px rgba(75,155,66,.18),var(--shadow);}
.theme-card.past{opacity:.6;}
.theme-icon{width:46px;height:46px;display:grid;place-items:center;border-radius:14px;background:#fff2cf;font-size:25px;}
.theme-info{min-width:0;}
.theme-name{font-size:13.5px;font-weight:950;line-height:1.25;}
.theme-period{margin-top:2px;font-size:11px;font-weight:900;color:#946c43;}
.theme-desc{margin-top:4px;font-size:11.5px;line-height:1.45;font-weight:800;color:#6f4f38;}
.theme-chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:6px;}
.theme-chips span{padding:3px 7px;border-radius:999px;background:#f3e2be;font-size:10px;font-weight:950;color:#6f4f38;}
.theme-state{display:inline-block;margin-left:5px;padding:2px 7px;border-radius:999px;font-size:9.5px;font-weight:950;background:#fff0ce;color:#805c35;vertical-align:middle;}
.theme-state.live{background:#eaf4df;color:#2f8b3a;}
.theme-state.past{background:#eee6da;color:#8a7a68;}
.theme-btn{min-width:62px;min-height:40px;border:0;border-radius:12px;background:#f0dfbc;color:#5c422f;font-size:11.5px;font-weight:950;}
.theme-btn.on{background:linear-gradient(90deg,#4a9b42,#75b84e);color:#fff;}
.upcoming{margin-top:9px;padding:14px;}
.upcoming-item{display:grid;grid-template-columns:34px 1fr;gap:8px;align-items:center;padding:9px 0;border-bottom:1px dashed rgba(122,87,51,.16);}
.upcoming-item:last-child{border-bottom:0;}
.upcoming-icon{font-size:22px;text-align:center;}
.upcoming-item strong{display:block;font-size:12.5px;}
.upcoming-item span{display:block;margin-top:2px;font-size:11px;color:#785a43;font-weight:800;line-height:1.4;}
.upcoming-empty{padding:6px 0;font-size:12px;color:#8a6a45;font-weight:850;line-height:1.5;}

/* ============================================================
   NEW PAGE 4 · 이벤트 (오늘의 발견 / 미션 / 사진첩)
   ============================================================ */
.event-tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin:0 0 9px;}
.event-tabs .reward-folder-btn{font-size:12px!important;padding:0 4px;white-space:nowrap;}
.found-top{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.found-card{padding:11px 10px;border:1px solid rgba(136,87,40,.14);border-radius:16px;background:rgba(255,248,231,.97);box-shadow:var(--shadow);display:flex;flex-direction:column;}
.found-card-title{display:flex;align-items:center;gap:5px;font-size:12.5px;font-weight:950;margin-bottom:8px;}
.found-photo{position:relative;height:92px;border-radius:12px;overflow:hidden;background:linear-gradient(145deg,#e9cfa8,#f7e6c9);display:grid;place-items:center;font-size:44px;}
.found-photo img{width:100%;height:100%;object-fit:cover;display:block;}
.found-name{margin-top:8px;font-size:13px;font-weight:950;color:#e07a1f;}
.found-name.done{color:#2f8b3a;}
.found-desc{margin-top:3px;font-size:11px;line-height:1.45;font-weight:800;color:#6f4f38;}
.found-meta{margin-top:5px;font-size:10.5px;font-weight:900;color:#7a5a3c;line-height:1.5;}
.found-btn{margin-top:auto;padding-top:8px;}
.found-btn button{width:100%;min-height:34px;border:0;border-radius:11px;background:#f0dfbc;color:#5c422f;font-size:11.5px;font-weight:950;}
.found-map{flex:1;min-height:150px;border-radius:12px;overflow:hidden;background:#fbf1de;border:1px solid rgba(124,83,43,.12);}
.found-map svg{width:100%;height:100%;display:block;}
.found-map-lock{
  min-height:150px;
  height:100%;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:7px;
  padding:16px 12px;
  text-align:center;
  color:#7a5a3c;
  background:linear-gradient(145deg,#fbf1de,#f5e3c3);
}
.found-map-lock .lock-icon{font-size:27px;line-height:1;}
.found-map-lock b{font-size:12.5px;font-weight:950;}
.found-map-lock span{font-size:10.5px;line-height:1.45;font-weight:850;color:#8a6a45;}
.found-btn button:disabled{
  opacity:.55;
  cursor:not-allowed;
  color:#8a7a68;
  background:#eadcc2;
}
.fm-room{fill:#f6e9d2;stroke:#c9ad82;stroke-width:2;}
.fm-room-active{fill:#fff3cf;}
.fm-focus{fill:none;stroke:#ef8c32;stroke-width:3;stroke-dasharray:5 4;}
.fm-label{fill:#7a5a3c;font-size:11px;font-weight:900;text-anchor:middle;}
.fm-pin{animation:float 1.6s ease-in-out infinite;}
.found-list{margin-top:9px;padding:13px 12px;}
.found-item{display:grid;grid-template-columns:48px 1fr auto;gap:9px;align-items:center;padding:9px 0;border-bottom:1px dashed rgba(122,87,51,.16);cursor:pointer;}
.found-item:last-child{border-bottom:0;}
.found-thumb{width:48px;height:48px;border-radius:12px;overflow:hidden;display:grid;place-items:center;background:#f5eddb;font-size:26px;}
.found-thumb img{width:100%;height:100%;object-fit:cover;display:block;}
.found-item strong{display:block;font-size:12.5px;}
.found-item span{display:block;margin-top:2px;font-size:11px;color:#785a43;font-weight:800;}
.found-right{text-align:right;font-size:10.5px;color:#7a5a3c;font-weight:900;line-height:1.55;white-space:nowrap;}
.found-item.done{opacity:.55;}
.mission-summary{padding:13px 14px;margin-bottom:9px;background:linear-gradient(145deg,#fff3cc,#ffd98a);display:flex;justify-content:space-between;align-items:center;gap:10px;}
.mission-summary .ms-title{font-size:13.5px;font-weight:950;}
.mission-summary .ms-desc{margin-top:3px;font-size:11px;font-weight:850;color:#76533b;line-height:1.45;}
.mission-summary .ms-count{flex:0 0 auto;text-align:center;padding:8px 12px;border-radius:12px;background:rgba(255,255,255,.7);font-size:10.5px;font-weight:950;color:#7a5a3c;}
.mission-summary .ms-count b{display:block;font-size:22px;color:#ef573f;line-height:1;margin-bottom:2px;}
.mission-card{padding:12px;margin-bottom:8px;border:1px solid rgba(136,87,40,.14);border-radius:16px;background:rgba(255,248,231,.97);box-shadow:var(--shadow);}
.mission-head{display:flex;align-items:center;gap:8px;}
.mission-head .m-icon{font-size:24px;}
.mission-head .m-name{font-size:13.5px;font-weight:950;flex:1;}
.mission-head .m-count{font-size:11px;font-weight:900;color:#7a5a3c;white-space:nowrap;}
.tier-row{display:grid;grid-template-columns:30px 1fr auto;gap:8px;align-items:center;margin-top:9px;}
.tier-medal{font-size:22px;text-align:center;filter:grayscale(1);opacity:.45;}
.tier-row.reached .tier-medal{filter:none;opacity:1;}
.tier-info{min-width:0;}
.tier-goal{font-size:11.5px;font-weight:950;}
.tier-track{height:7px;margin-top:4px;border-radius:10px;overflow:hidden;background:#ead9b9;}
.tier-fill{height:100%;border-radius:inherit;background:linear-gradient(90deg,#ff8e33,#ffca43);transition:width .3s;}
.tier-btn{min-width:78px;min-height:34px;border:0;border-radius:11px;background:#f0dfbc;color:#8a7a68;font-size:11px!important;font-weight:950;padding:0 8px;}
.tier-btn.claim{background:linear-gradient(90deg,#4a9b42,#75b84e);color:#fff;animation:pulseBtn 1.4s ease-in-out infinite;}
.tier-btn.claimed{background:#eaf4df;color:#2f8b3a;}
@keyframes pulseBtn{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
.photo-info{padding:12px 13px;margin-bottom:9px;display:flex;justify-content:space-between;align-items:center;gap:8px;}
.photo-info .p-title{font-size:13.5px;font-weight:950;}
.photo-info .p-desc{margin-top:3px;font-size:11px;font-weight:800;color:#76533b;line-height:1.45;}
.photo-info .p-count{flex:0 0 auto;text-align:center;padding:8px 10px;border-radius:12px;background:#fff2cf;font-size:10.5px;font-weight:950;color:#7a5a3c;}
.photo-info .p-count b{display:block;font-size:20px;color:#ef573f;line-height:1;margin-bottom:2px;}
.photo-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.photo-tile{position:relative;border-radius:16px;overflow:hidden;background:#f5eddb;box-shadow:var(--shadow);cursor:pointer;aspect-ratio:1/1;}
.photo-tile.wide{grid-column:1 / -1;aspect-ratio:2.12/1;}
.photo-tile.wide img{object-fit:cover;}
.photo-tile img{width:100%;height:100%;object-fit:cover;display:block;}
.photo-tile .ph-emoji{width:100%;height:100%;display:grid;place-items:center;font-size:56px;background:linear-gradient(145deg,#f6e3ba,#fff7e4);}
.photo-cap{position:absolute;left:0;right:0;bottom:0;padding:16px 9px 8px;background:linear-gradient(180deg,transparent,rgba(45,33,23,.74));color:#fff;font-size:11px;font-weight:950;line-height:1.3;}
.photo-cap small{display:block;font-weight:800;opacity:.85;font-size:9.5px;}
.photo-empty{padding:14px;margin-top:9px;text-align:center;font-size:11.5px;line-height:1.6;font-weight:850;color:#6f4f38;}
.photo-empty code{background:#fff2cf;padding:2px 6px;border-radius:6px;font-size:11px;}
.nav-dot{display:inline-block;width:7px;height:7px;margin-left:3px;border-radius:50%;background:#ffd44f;vertical-align:middle;box-shadow:0 0 0 2px rgba(255,212,79,.25);}

/* ===== Home information architecture: Map / AI preparation / Manual cleaning ===== */
.home-section{
  margin-bottom:10px;
  padding:13px 11px;
  overflow:hidden;
}
.home-section-head{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:10px;
  margin-bottom:10px;
}
.home-section-kicker{
  margin-bottom:3px;
  color:#a27145;
  font-size:9px;
  line-height:1;
  font-weight:950;
  letter-spacing:1.1px;
}
.home-section-title{
  color:#4b3324;
  font-size:16px;
  line-height:1.25;
  font-weight:1000;
}
.home-section-badge{
  flex:0 0 auto;
  padding:6px 9px;
  border-radius:999px;
  background:#f3e4c5;
  color:#76553e;
  font-size:10.5px;
  line-height:1;
  font-weight:950;
}
.home-section-badge.ready{background:#e7f4d9;color:#2f8b3a;}
.home-section-badge.learning{background:#fff0ca;color:#e07c22;}
.map-section{background:rgba(255,248,231,.98);}
.map-section-content{width:100%;}
.map-empty-state{
  min-height:138px;
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  gap:6px;
  padding:17px 12px;
  border:1px dashed rgba(124,83,43,.24);
  border-radius:15px;
  background:linear-gradient(145deg,#fff8e6,#f4e3bf);
  color:#7a5a3c;
  text-align:center;
}
.map-empty-state.learning{border-style:solid;background:linear-gradient(145deg,#fff5d9,#f5dfae);}
.map-empty-icon{font-size:31px;line-height:1;}
.map-empty-state b{color:#4b3324;font-size:13px;font-weight:1000;}
.map-empty-state span:last-child{font-size:11px;line-height:1.5;font-weight:850;}
.map-section .home-map-card{
  margin:0;
  padding:0;
  border:0;
  border-radius:0;
  background:transparent;
  box-shadow:none;
}
.map-section .home-map-head{margin:0 0 7px;}
/* 맵 색상 범례: 학습 완료 후 지도 바로 아래에 항상 표시 */
.map-section .map-legend{
  margin-top:8px;
  padding:8px 6px;
  border-radius:13px;
  background:rgba(255,250,235,.88);
  font-size:11px;
  gap:6px 9px;
}
.map-section .map-legend-title{font-size:11px;font-weight:800;}
.map-section .map-legend-item{font-size:10.5px;font-weight:700;gap:4px;}
.map-section .map-dot{width:10px;height:10px;}
.room .mode-chip{display:none!important;}
.prep-section{margin-bottom:10px!important;}
.prep-section .plan-head{align-items:center;}
.prep-section .learn-panel{margin-bottom:0;}
.direct-clean-section{
  margin:0!important;
  padding:13px 11px!important;
  border-radius:17px!important;
  background:rgba(255,248,231,.98)!important;
  box-shadow:var(--shadow);
}
.direct-clean-section .home-section-kicker{margin-bottom:4px;}
.direct-clean-section .condition-title{
  margin-bottom:9px!important;
  color:#4b3324!important;
  font-size:16px!important;
  font-weight:1000!important;
}
.direct-clean-section.condition-panel.manual-mode{margin-top:0!important;}
.direct-clean-section.condition-panel.manual-mode .condition-title:before{content:none!important;}


/* ===== Home visual adjustment: bigger station + mission moved right ===== */
#homePage .house{
  left:76px!important;
  top:112px!important;
  width:94px!important;
  height:80px!important;
  border-radius:38px 38px 9px 9px!important;
  box-shadow:0 8px 14px rgba(54,36,23,.24)!important;
}
#homePage .house:before{
  left:27px!important;
  bottom:0!important;
  width:40px!important;
  height:44px!important;
  border-radius:20px 20px 0 0!important;
}
#homePage .house:after{
  top:13px!important;
  left:27px!important;
  font-size:8.5px!important;
  letter-spacing:.2px!important;
}
#homePage .mission{
  left:auto!important;
  right:10px!important;
  bottom:14px!important;
  width:96px!important;
  z-index:18!important;
}



/* ===== Typography refinement: Pretendard + NanumSquare Neo-like hierarchy ===== */
html,body,button,input,select{
  font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",Arial,sans-serif!important;
  font-synthesis:none;
}
body{font-weight:500!important;letter-spacing:-.018em;}

/* 큰 제목: 또렷하지만 과하게 두껍지 않게 */
.app-title,
.section-title,
.home-section-title,
.modal-title{
  font-weight:800!important;
  letter-spacing:-.035em!important;
}

/* 소제목/카드 제목 */
.brand,
.panel-title,
.plan-title,
.learn-title,
.condition-title,
.mini-title,
.reward-title,
.sched-title,
.sub-title,
.theme-name,
.found-card-title,
.found-name,
.mission-summary .ms-title,
.mission-head .m-name,
.photo-info .p-title,
.note-title,
.summary-title,
.mission-title{
  font-weight:700!important;
  letter-spacing:-.025em!important;
}

/* 버튼/탭/선택 UI */
button,
.nav-btn,
.reward-btn,
.reward-folder-btn,
.scope-btn,
.learn-btn,
.predict-btn,
.clean-execute-btn,
.start-clean-primary,
.manual-clean-btn,
.manual-combo-btn,
.map-action-btn,
.sched-opt,
.day-chip,
.theme-btn,
.tier-btn,
.condition-select,
.coin-pill,
.badge,
.home-section-badge,
.plan-model,
.learn-pill,
.profile-chip{
  font-weight:700!important;
  letter-spacing:-.02em!important;
}

/* 일반 설명문: 나눔스퀘어 네오와 비슷한 가벼운 본문 질감 */
.modal-body,
.reward-desc,
.care-lead,
.care-note,
.sched-desc,
.theme-desc,
.found-desc,
.photo-info .p-desc,
.condition-help,
.learn-desc,
.first-learn-note,
.plan-summary,
.battery-info,
.battery-message,
.time-tip,
.event-content span,
.flow-guide,
.map-action-hint,
.map-recommend-card,
.map-prep-sub,
.found-map-lock span,
.upcoming-item span,
.mission-summary .ms-desc,
.note-caption{
  font-weight:500!important;
  letter-spacing:-.018em!important;
}

/* 수치·핵심 상태는 시선이 가도록 한 단계만 강조 */
.plan-soc-value,
.care-stat b,
.robot-soc-badge b,
.time-number,
.summary-val.em,
.ms-count b,
.p-count b{
  font-weight:800!important;
}

strong,b{font-weight:700;}



/* ===== Compact AI cleaning card: simplified for quick use ===== */
#aiCleanSection.ai-ready{
  padding:12px 11px 13px!important;
}
#aiCleanSection.ai-ready .plan-head{
  margin-bottom:9px!important;
}
#aiCleanSection.ai-ready .plan-title{
  font-size:15px!important;
  font-weight:800!important;
}
#aiCleanSection.ai-ready .plan-model{
  padding:5px 8px!important;
  font-size:10px!important;
  border-radius:999px!important;
  background:#e7f4d9!important;
  color:#2f8b3a!important;
}
#aiMappedControls.ai-clean-controls{
  display:block;
}
#aiCleanSection .ai-clean-intro{
  display:flex!important;
  align-items:center!important;
  gap:7px!important;
  margin:0 0 10px!important;
  padding:8px 10px!important;
  border:0!important;
  border-radius:11px!important;
  background:#f3f8ed!important;
  box-shadow:none!important;
}
#aiCleanSection .ai-clean-intro-icon{
  display:inline!important;
  width:auto!important;
  height:auto!important;
  flex:0 0 auto!important;
  background:transparent!important;
  font-size:15px!important;
  line-height:1!important;
}
#aiCleanSection .ai-clean-intro-title{
  color:#5e4632!important;
  font-size:11.5px!important;
  line-height:1.35!important;
  font-weight:600!important;
  letter-spacing:-.15px!important;
}
#aiCleanSection .ai-clean-intro-desc{display:none!important;}
#aiCleanSection .ai-clean-mode-row{
  display:grid!important;
  grid-template-columns:repeat(3,minmax(0,1fr))!important;
  gap:7px!important;
}
#aiCleanSection .ai-clean-mode-btn{
  display:flex!important;
  flex-direction:column!important;
  align-items:center!important;
  justify-content:center!important;
  gap:4px!important;
  min-width:0!important;
  min-height:62px!important;
  padding:7px 3px!important;
  border:1px solid #ead9b7!important;
  border-radius:14px!important;
  background:#fffaf0!important;
  color:#5a412e!important;
  box-shadow:0 3px 8px rgba(79,48,21,.08)!important;
  font-size:10.5px!important;
  line-height:1.15!important;
  font-weight:700!important;
  white-space:nowrap!important;
  word-break:keep-all!important;
}
#aiCleanSection .ai-clean-mode-btn .ai-mode-icon{
  display:block!important;
  font-size:20px!important;
  line-height:1!important;
}
#aiCleanSection .ai-clean-mode-btn.active{
  border-color:transparent!important;
  background:linear-gradient(180deg,#64b84e,#47a342)!important;
  color:#fff!important;
  box-shadow:0 6px 12px rgba(67,126,56,.20)!important;
}
#aiCleanSection .ai-clean-mode-btn.danger.active{
  background:linear-gradient(180deg,#f28f49,#e87539)!important;
  color:#fff!important;
}
#aiCleanSection .ai-clean-selection-note{
  min-height:0!important;
  margin:8px 1px 0!important;
  padding:0!important;
  border:0!important;
  border-radius:0!important;
  background:transparent!important;
  color:#84684e!important;
  font-size:10px!important;
  line-height:1.35!important;
  font-weight:500!important;
  text-align:center!important;
}
#aiCleanSection .ai-clean-selection-note b{
  color:#5e4632!important;
  font-weight:600!important;
}
#aiCleanSection .ai-clean-now-btn{
  display:flex!important;
  align-items:center!important;
  justify-content:center!important;
  width:100%!important;
  min-height:48px!important;
  margin-top:10px!important;
  padding:0 12px!important;
  border:0!important;
  border-radius:14px!important;
  background:linear-gradient(90deg,#f18b2e,#f6a342)!important;
  color:#fff!important;
  box-shadow:0 7px 14px rgba(210,117,35,.22)!important;
  font-size:14px!important;
  line-height:1.1!important;
  font-weight:800!important;
  letter-spacing:-.2px!important;
}
#aiCleanSection .ai-clean-now-btn .ai-clean-now-main{display:inline!important;}
#aiCleanSection .ai-clean-now-btn #aiCleanNowSub{display:none!important;}
@media(max-width:360px){
  #aiCleanSection .ai-clean-mode-btn{font-size:9.8px!important;min-height:58px!important;}
  #aiCleanSection .ai-clean-mode-btn .ai-mode-icon{font-size:18px!important;}
}

/* ===== Home · Battery preparation strategy selector ===== */
.battery-strategy-section{
  margin-bottom:10px;
  padding:14px 12px;
  background:rgba(255,248,231,.98);
}
.battery-strategy-section .home-section-kicker{font-size:11.5px!important;line-height:1.15!important;letter-spacing:1px!important;}
.battery-strategy-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:9px;}
.battery-strategy-section-title{color:#4b3324;font-size:18px;line-height:1.25;font-weight:800;}
.battery-strategy-badge{padding:6px 10px;border-radius:999px;background:#edf7e4;color:#2f8b3a;font-size:11px;font-weight:750;white-space:nowrap;}
.battery-strategy-row{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.battery-strategy-btn{
  min-height:72px;padding:10px 8px;border:1px solid #ead9b7;border-radius:14px;background:#fff;color:#60452f;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;text-align:center;box-shadow:0 3px 7px rgba(79,48,21,.06);
}
.battery-strategy-btn .strategy-main{font-size:13.5px;line-height:1.25;font-weight:750;word-break:keep-all;}
.battery-strategy-btn .strategy-sub{font-size:10.5px;line-height:1.3;font-weight:500;color:#8a6a45;word-break:keep-all;}
.battery-strategy-btn.active{border-color:transparent;background:linear-gradient(180deg,#64b84e,#47a342);color:#fff;box-shadow:0 6px 12px rgba(67,126,56,.18);}
.battery-strategy-btn.active .strategy-sub{color:rgba(255,255,255,.9);}
.battery-strategy-btn.ready.active{background:linear-gradient(180deg,#f1a23d,#ed842b);box-shadow:0 6px 12px rgba(210,117,35,.18);}
.battery-strategy-btn:disabled{opacity:.55;cursor:not-allowed;}
.battery-strategy-note{margin-top:9px;padding:8px 9px;border-radius:10px;background:#fff7e5;color:#765b43;font-size:11.5px;line-height:1.45;font-weight:500;text-align:center;word-break:keep-all;}
.battery-strategy-note b{color:#2f8b3a;font-weight:750;}

</style>
</head>

<body>
<div class="phone">
  <div class="notch"></div>
  <div class="screen">

    <header class="header">
      <div class="header-top">
        <div>
          <div class="brand">LG ROBO CARE</div>
          <div class="app-title">홈지니 키우기</div>
        </div>
        <div class="coin-pill">🪙 <span id="coinText">050</span></div>
      </div>
      <nav class="nav">
        <button class="nav-btn active" data-page="homePage">홈</button>
        <button class="nav-btn" data-page="batteryPage">부품케어</button>
        <button class="nav-btn" data-page="recordPage">예약청소</button>
        <button class="nav-btn" data-page="eventPage">이벤트<span class="nav-dot" id="eventNavDot" style="display:none"></span></button>
        <button class="nav-btn" data-page="rewardPage">리워드</button>
      </nav>
    </header>

    <main class="pages">

      <section class="page active" id="homePage">
        <div class="room" id="room">
          <div class="wall-light"></div><div class="floor"></div>
          <div class="plant">🪴</div><div class="house"></div><div class="sofa"></div>
          <div class="speech" id="speech"><strong>배가 든든해요!</strong><br>청소를 준비할게요!</div>
          <div class="mode-chip" id="modeChip">✨ 홈지니 맞춤 준비</div>
          <div class="rug"></div>
          <div class="clean-path"><div class="clean-fill" id="cleanFill"></div></div>
          <div class="charge-ring"></div>
          <div class="dust"><span></span><span></span><span></span><span></span><span></span><span></span></div>

          <div class="robot" id="robot" data-action="pet">
            <div class="robot-aura-deco" id="robotAuraDeco"><span>✨</span><span>✨</span><span>✨</span><span>✨</span></div>
            <div class="crown">👑</div>
            <div class="robot-accessory robot-head-deco" id="robotHeadDeco"></div>
            <div class="spark" id="spark">✨</div><div class="robot-top"></div>
            <div class="face">
              <div class="eye left"></div><div class="eye right"></div>
              <div class="cheek left"></div><div class="cheek right"></div><div class="mouth"></div>
            </div>
            <div class="robot-accessory robot-body-deco" id="robotBodyDeco"></div>
            <div class="slot"></div>
          </div>
          <div class="robot-soc-badge" id="robotSocBadge"><button type="button" class="battery-help-btn" data-action="batteryCoachInfo" aria-label="배터리 코칭 안내 보기">!</button><span>🔋 현재 배터리</span><b>20%</b></div>

          <div class="mission">
            <div class="mission-title">오늘의 미션</div>
            <div class="mission-text">거실 청소 1회 완료하기</div>
            <div class="mission-progress">
              <div class="mission-track"><div class="mission-fill" id="missionFill"></div></div>
              <span class="reward-small">+50</span>
            </div>
          </div>

          <div class="effect-layer" id="effectLayer"></div>
        </div>

        <div class="home-dashboard">

          <section class="panel home-section map-section" aria-labelledby="mapSectionTitle">
            <div class="home-section-head">
              <div>
                <div class="home-section-kicker">CLEANING MAP</div>
                <div class="home-section-title" id="mapSectionTitle">🗺️ 맵</div>
              </div>
              <div class="home-section-badge" id="mapSectionBadge">학습 전</div>
            </div>
            <div class="map-section-content" id="mapSectionContent">
              <div class="map-empty-state">
                <span class="map-empty-icon">🏠</span>
                <b>우리 집 맵을 준비하고 있어요</b>
                <span>맞춤 청소 준비에서 1회차 학습을 시작하면<br>방 구조와 바닥 상태가 여기에 표시돼요.</span>
              </div>
            </div>
          </section>

          <!-- AI 맞춤청소와 직접조건청소에 공통 적용되는 배터리 준비 모드 -->
          <section class="panel battery-strategy-section" id="batteryStrategySection" aria-labelledby="batteryStrategySectionTitle">
            <div class="battery-strategy-head">
              <div>
                <div class="home-section-kicker">BATTERY MODE</div>
                <div class="battery-strategy-section-title" id="batteryStrategySectionTitle">🔋 배터리 준비 모드</div>
              </div>
              <div class="battery-strategy-badge" id="batteryStrategyBadge">케어 우선</div>
            </div>
            <div class="battery-strategy-row">
              <button type="button" class="battery-strategy-btn" id="batteryStrategyCareBtn" data-action="batteryStrategyCare">
                <span class="strategy-main">🌱 배터리 케어 우선</span>
                <span class="strategy-sub">필요한 만큼만 충전</span>
              </button>
              <button type="button" class="battery-strategy-btn ready" id="batteryStrategyReadyBtn" data-action="batteryStrategyReady">
                <span class="strategy-main">⚡ 청소 준비 우선</span>
                <span class="strategy-sub">여유 있게 미리 준비</span>
              </button>
            </div>
            <div class="battery-strategy-note" id="batteryStrategyNote"><b>배터리 케어 우선</b> · 청소에 필요한 만큼만 충전해요.</div>
          </section>

          <section class="panel plan-panel prep-section" id="aiCleanSection" aria-labelledby="prepSectionTitle">
            <div class="plan-head">
              <div>
                <div class="home-section-kicker">AI SMART CLEANING</div>
                <div class="plan-title" id="prepSectionTitle">🤖 우리집 AI 맞춤청소</div>
              </div>
              <div class="plan-model" id="planModel">1회차 학습 전</div>
            </div>

            <!-- 매핑 전/학습 중에만 보이는 최초 학습 영역 -->
            <div class="learn-panel" id="learnPanel">
              <div class="learn-top">
                <div class="learn-title" id="learnTitle">처음 사용할 때는 홈지니가 집을 먼저 배워요</div>
                <div class="learn-pill" id="learnPill">초기 학습</div>
              </div>
              <div class="learn-desc" id="learnDesc">처음 한 번만 집 구조와 바닥 상태를 배워요.</div>
              <div class="learn-progress"><div class="learn-fill" id="learnFill"></div></div>
              <div class="learn-status" id="learnStatus">1회차 학습 청소를 시작하면 홈지니가 집 구조와 구역 정보를 자동으로 기록해요.</div>
              <div class="learn-steps" id="learnSteps"></div>
              <div class="learn-actions" id="learnActions">
                <button type="button" class="learn-btn" id="learnBtn" data-action="startFirstMapping" onpointerdown="window.__forceStartFirstMapping && window.__forceStartFirstMapping(event);" onmousedown="window.__forceStartFirstMapping && window.__forceStartFirstMapping(event);" ontouchstart="window.__forceStartFirstMapping && window.__forceStartFirstMapping(event);" onclick="window.__forceStartFirstMapping && window.__forceStartFirstMapping(event);">🏠 1회차 학습 청소 시작</button>
                <button type="button" class="clean-execute-btn" id="cleanExecuteBtn" data-action="executeTopClean" style="display:none;">🧹 청소하기</button>
              </div>
            </div>

            <!-- 매핑 완료 후에는 복잡한 학습 결과 대신 이 간단한 AI 청소 UI만 표시 -->
            <div class="ai-clean-controls" id="aiMappedControls">
              <div class="ai-clean-intro">
                <span class="ai-clean-intro-icon">✨</span>
                <div class="ai-clean-intro-title">매핑한 우리 집에 맞춰 홈지니가 알아서 청소해요.</div>
              </div>

              <div class="ai-clean-mode-row">
                <button type="button" class="ai-clean-mode-btn" id="aiHomeCleanBtn" data-action="aiAutoClean"><span class="ai-mode-icon">🏠</span><span>집 전체청소</span></button>
                <button type="button" class="ai-clean-mode-btn" id="aiDirtyCleanBtn" data-action="dirtyOnlyClean"><span class="ai-mode-icon">🔥</span><span>더러운곳만</span></button>
                <button type="button" class="ai-clean-mode-btn danger" id="aiNoGoBtn" data-action="toggleNoGoMode"><span class="ai-mode-icon">🚫</span><span>금지구역설정</span></button>
              </div>

              <div class="ai-clean-selection-note" id="aiCleanSelectionNote">집 전체를 AI가 알아서 청소해요.</div>

              <button type="button" class="ai-clean-now-btn" id="aiCleanNowBtn" data-action="executeTopClean">
                <span class="ai-clean-now-main">🧹 바로 청소하기</span>
                <span id="aiCleanNowSub">선택한 방식으로 바로 시작해요</span>
              </button>
            </div>

            <!-- 기존 계산/상태 연결을 유지하기 위한 숨김 데이터 영역 -->
            <div class="scope-buttons" aria-hidden="true">
              <button class="scope-btn active" id="scopeHome" data-action="selectHome">집 전체</button>
              <button class="scope-btn" id="scopeZone1" data-action="selectZone1">1구역</button>
              <button class="scope-btn" id="scopeZone2" data-action="selectZone2">2구역</button>
              <button class="scope-btn" id="scopeZone3" data-action="selectZone3">3구역</button>
              <button class="scope-btn" id="scopeZone4" data-action="selectZone4">4구역</button>
              <button class="scope-btn" id="scopeZone5" data-action="selectZone5">5구역</button>
            </div>
            <div class="selected-plan" aria-hidden="true">
              <div class="plan-summary" id="planSummary">집 전체 청소 조건을 분석 중입니다.</div>
              <div class="plan-soc">
                <div class="plan-soc-label">충전 준비</div>
                <div class="plan-soc-value"><span id="planTargetSoc">81</span>%</div>
                <div class="plan-soc-sub" id="planSocSub">필요한 만큼만 충전</div>
              </div>
            </div>
            <button class="start-clean-primary" id="startCleanPrimary" data-action="clean" disabled aria-hidden="true">
              🧹 청소 미션 수행하기
              <small id="startCleanHint">준비가 끝나면 바로 시작할 수 있어요</small>
            </button>
          </section>

          <section class="panel condition-panel direct-clean-section" id="conditionPanel" aria-labelledby="conditionTitle">
              <div class="home-section-kicker">MANUAL CLEANING</div>
              <div class="condition-title" id="conditionTitle">✍️ 직접 조건 청소</div>

              <div id="firstLearnInputs">
                <div class="condition-help first-learn-note compact-note">
                  <div class="note-title">맞춤 청소 준비 후 사용할 수 있어요</div>
                  <div class="note-caption">먼저 위의 1회차 학습을 완료하면 청소 범위·방식·강도·오늘 상태를 직접 선택할 수 있어요.</div>
                </div>
              </div>

              <div id="predictionInputs" style="display:none;">
                <div class="condition-help">세부 조건을 직접 고르면 홈지니가 준비부터 청소까지 이어서 진행해요.</div>
                <div class="predict-condition-grid">
                  <label for="scopeSelect">청소 범위</label>
                  <select class="condition-select" id="scopeSelect">
                    <option value="home">집 전체</option>
                    <option value="1">1구역</option>
                    <option value="2">2구역</option>
                    <option value="3">3구역</option>
                    <option value="4">4구역</option>
                    <option value="5">5구역</option>
                  </select>
                  <label for="cleanModeSelect">청소 방식</label>
                  <select class="condition-select" id="cleanModeSelect">
                    <option value="dry">건식</option>
                    <option value="mop">물걸레</option>
                    <option value="both">건식+물걸레</option>
                  </select>
                  <label for="intensitySelect">청소 강도</label>
                  <select class="condition-select" id="intensitySelect">
                    <option value="fast">빠른</option>
                    <option value="standard" selected>표준</option>
                    <option value="careful">꼼꼼</option>
                  </select>
                  <label for="todayStateSelect">오늘 상태</label>
                  <select class="condition-select" id="todayStateSelect">
                    <option value="normal">평소와 같음</option>
                    <option value="dust">먼지 많음</option>
                    <option value="pet">반려동물 털 많음</option>
                    <option value="obstacle">바닥 물건 많음</option>
                  </select>
                </div>
              </div>

              <button class="predict-btn manual-combo-btn" id="predictBtn" data-action="manualCleanAndGo">🔥 선택 조건으로 준비하고 청소하기</button>
              <div class="predict-loading" id="predictLoading">1회차 학습 청소가 끝나면 오늘 청소 준비를 할 수 있어요.</div>
              <div class="flow-guide" id="flowGuide"><span class="guide-step">현재 단계</span>1회차 학습 청소로 집 정보를 먼저 저장해 주세요.</div>
          </section>

          <div class="actions">
            <button class="action-btn" data-action="feed"><span class="action-icon">🥣</span>먹여주기</button>
            <button class="action-btn" data-action="play"><span class="action-icon">🏐</span>놀아주기</button>
            <button class="action-btn" data-action="train"><span class="action-icon">🏋️</span>훈련하기</button>
            <button class="action-btn" data-action="photo"><span class="action-icon">📷</span>사진첩</button>
            <button class="action-btn" data-action="clean"><span class="action-icon">🏆</span>미션</button>
            <button class="action-btn" data-action="shop"><span class="action-icon">🛒</span>상점</button>
          </div>

          <div class="home-cards">
            <section class="mini-card">
              <div class="mini-title">배터리 컨디션</div>
              <div class="battery-info">너무 배부르거나<br>너무 배고프지 않게<br>홈지니가 알아서 관리해요!</div>
              <div class="battery-face" id="batteryFace">😊</div>
              <div class="scale"><div class="pointer" id="pointer"></div></div>
              <div class="scale-labels"><span>0%</span><span>15%</span><span>90%</span><span>100%</span></div>
              <div class="battery-message" id="batteryMessage">배터리 컨디션이 좋아요.</div>
            </section>

            <section class="mini-card time-card">
              <div class="mini-title">필요 청소 가능 시간</div>
              <div class="time-icon">🤖</div>
              <div class="time-number"><span id="cleanTime">45</span><small> 분</small></div>
              <div class="time-sub">현재 배터리 기준</div>
              <div class="time-tip" id="timeTip">현재 배터리로 청소가 가능합니다.</div>
            </section>

            <section class="mini-card food-card">
              <div class="food-title">오늘의 음식</div><div class="food-bowl"></div>
              <div class="food-count">보유량: <span id="foodText">1</span>개</div>
            </section>
          </div>
        </div>
      </section>

      <!-- ===================== PAGE 2 · 부품 케어 ===================== -->
      <section class="page" id="batteryPage">
        <div class="section-kicker">PARTS CARE</div>
        <div class="section-title">부품 케어</div>

        <!-- 1. 배터리 케어 -->
        <div class="panel battery-care-main">
          <div class="battery-care-head">
            <div>
              <div class="battery-care-kicker">BATTERY CARE</div>
              <div class="battery-care-title">🔋 배터리 케어</div>
            </div>
            <div class="battery-care-badge">자동 케어</div>
          </div>

          <div class="battery-care-copy">
            100% 완충을 반복하지 않고 <b>청소에 필요한 만큼만 충전</b>하며,<br>
            15% 아래로 내려가기 전에 쉬어가도록 관리해요.
          </div>

          <div class="battery-health-card">
            <div class="battery-health-top">
              <div>
                <div class="battery-health-label">현재 배터리 건강도</div>
                <div class="battery-health-state" id="careHealthState">매우 좋음</div>
              </div>
              <div class="battery-health-value" id="careHealthText">100%</div>
            </div>
            <div class="care-health-track battery-health-track">
              <div class="care-health-fill" id="careHealthFill" style="width:100%"></div>
            </div>
          </div>

          <div class="care-stats battery-care-stats">
            <div class="care-stat"><span>맞춤 충전</span><b id="careAcceptText">5</b><small>회</small></div>
            <div class="care-stat"><span>15% 잔량 보호</span><b id="careReserveText">1</b><small>회</small></div>
          </div>

          <div class="battery-life-guide">
            <div class="battery-life-guide-icon">🗓️</div>
            <div class="battery-life-guide-copy">
              <b>약 3년 주기로 점검·교체를 권장해요</b>
              <div class="battery-life-usage-row"><span class="battery-use-day" id="batteryUseDay">사용 D+1일째</span></div>
              <div class="battery-life-sub">사용에 불편이 없다면 3년 이상 사용할 수도 있어요.</div>
            </div>
            <button type="button" class="battery-life-guide-btn" data-action="batteryLifeInfo">자세히</button>
          </div>

          <div class="care-note" id="careNote">오늘도 과충전 없이 관리 중이에요.</div>
        </div>

        <!-- 2. 현재 부품 상태 -->
        <div class="care-subhead"><span>현재 부품 상태</span><small>누르면 상세 확인</small></div>
        <div class="parts-grid" id="partsGrid"></div>

        <!-- 3. 실시간 케어 기록 -->
        <div class="panel events care-events-panel">
          <div class="panel-head"><div class="panel-title">실시간 케어 기록</div><div class="badge">자동 기록</div></div>
          <div id="eventList">
            <div class="event-item"><div class="event-time">14:20</div><div class="event-content"><strong>맞춤 충전 완료<span class="event-tag">배터리 보호</span></strong><span>청소에 필요한 만큼만 충전하고 멈췄어요.</span></div></div>
            <div class="event-item"><div class="event-time">10:15</div><div class="event-content"><strong>청소 준비 완료<span class="event-tag">맞춤 관리</span></strong><span>우리 집 상태에 맞춰 필요한 배터리를 계산했어요.</span></div></div>
          </div>
        </div>
      </section>

      <!-- ===================== PAGE 3 · 예약 청소 ===================== -->
      <section class="page" id="recordPage">
        <div class="section-kicker">SMART SCHEDULE</div>
        <div class="section-title">출퇴근 맞춤 예약 청소</div>

        <div class="panel sched-panel">
          <div class="sched-head">
            <div>
              <div class="sched-title">🚶 출퇴근 맞춤 예약</div>
              <div class="sched-desc">집을 비우는 시간에만 청소하고, 돌아오기 전에 조용히 도킹해 두어요.</div>
            </div>
            <button class="switch" id="commuteSwitch" data-action="toggleCommute" aria-label="출퇴근 예약 켜기"><span class="knob"></span></button>
          </div>
          <div class="sched-body off" id="commuteBody">
            <div class="time-row">
              <label for="leaveTime">출근</label>
              <select class="condition-select" id="leaveTime"></select>
              <label for="returnTime">퇴근</label>
              <select class="condition-select" id="returnTime"></select>
            </div>
            <div class="day-chips" id="dayChips"></div>
            <div class="sched-options">
              <button class="sched-opt active" id="commuteAfter" data-action="commuteMode" data-mode="after">출근 30분 뒤 시작</button>
              <button class="sched-opt" id="commuteBefore" data-action="commuteMode" data-mode="before">퇴근 1시간 전 마무리</button>
            </div>
          </div>
          <div class="sched-preview off" id="commutePreview">스위치를 켜면 출퇴근 시간에 맞춘 예약이 만들어져요.</div>
        </div>

        <div class="sub-title">🎎 테마별 기간 청소</div>
        <div class="theme-list" id="themeList"></div>

        <div class="panel upcoming">
          <div class="panel-head"><div class="panel-title">다가오는 예약</div><div class="badge" id="upcomingBadge">0건</div></div>
          <div id="upcomingList"></div>
        </div>
      </section>

      <!-- ===================== PAGE 4 · 이벤트 ===================== -->
      <section class="page" id="eventPage">
        <div class="section-kicker">DISCOVERY & MISSION</div>
        <div class="section-title">이벤트</div>

        <div class="event-tabs">
          <button class="reward-folder-btn active" id="evTabFound" data-action="evTabFound">🔍 오늘의 발견</button>
          <button class="reward-folder-btn" id="evTabMission" data-action="evTabMission">🏅 미션</button>
          <button class="reward-folder-btn" id="evTabPhoto" data-action="evTabPhoto">📷 사진첩</button>
        </div>

        <div class="reward-panel" id="evFoundPanel">
          <div class="found-top">
            <div class="found-card" id="foundTodayCard"></div>
            <div class="found-card">
              <div class="found-card-title">📍 발견 위치 보기</div>
              <div class="found-map" id="foundMap"></div>
              <div class="found-btn"><button type="button" id="foundMapBigBtn" data-action="foundMapBig">지도 크게 보기 ›</button></div>
            </div>
          </div>
          <div class="panel found-list">
            <div class="panel-head"><div class="panel-title">📋 최근 발견 기록</div><div class="badge" id="foundCountBadge">전체 3건</div></div>
            <div id="foundList"></div>
          </div>
        </div>

        <div class="reward-panel hidden" id="evMissionPanel">
          <div class="panel mission-summary">
            <div>
              <div class="ms-title">도전과제 메달</div>
              <div class="ms-desc">목표를 달성하면 메달과 코인을 받아요.<br>받은 코인은 리워드에서 쓸 수 있어요.</div>
            </div>
            <div class="ms-count"><b id="missionClaimable">0</b>받을 보상</div>
          </div>
          <div id="missionList"></div>
        </div>

        <div class="reward-panel hidden" id="evPhotoPanel">
          <div class="panel photo-info">
            <div>
              <div class="p-title">📷 홈지니 사진첩</div>
              <div class="p-desc">청소 중 움직이는 친구를 만나면 홈지니가 살짝 찍어둬요. 혼자 있는 반려동물의 하루를 볼 수 있어요.</div>
            </div>
            <div class="p-count"><b id="photoCount">0</b>장</div>
          </div>
          <div class="photo-grid" id="photoGrid"></div>
          <div class="panel photo-empty" id="photoEmpty" style="display:none;">
            지금은 예시 사진이에요.<br>실제 사진을 넣으려면 <code>assets/photos/dog1.jpg</code>, <code>dog2.jpg</code>, <code>dog3_jpg</code>를 넣어주세요.
          </div>
        </div>
      </section>

      <!-- ===================== PAGE 5 · 리워드 (원본 유지) ===================== -->
      <section class="page" id="rewardPage">
        <div class="section-kicker">REWARD</div>
        <div class="section-title">홈지니 성장 리워드</div>

        <div class="reward-folder-tabs">
          <button class="reward-folder-btn active" id="rewardTabItems" data-action="rewardTabItems">꾸미기 아이템</button>
          <button class="reward-folder-btn" id="rewardTabCoupons" data-action="rewardTabCoupons">LG 혜택 쿠폰</button>
        </div>

        <div class="reward-panel" id="rewardItemsPanel">
          <div class="reward-grid">
            <div class="reward-card seasonal-card" id="cardSanta"><div class="reward-icon santa-reward-icon"><img src="__SANTA_HAT_DATA_URI__" alt="산타클로스 모자"></div><div class="reward-title">산타클로스 모자</div><div class="reward-desc">크리스마스 에디션! 홈지니에게 포근한 산타 모자를 씌워줘요.</div><div class="reward-status" id="statusSanta"></div><button class="reward-btn" id="btnSanta" data-action="itemSanta">50 코인</button></div>
            <div class="reward-card" id="cardRibbon"><div class="reward-icon">🎀</div><div class="reward-title">빨간 리본</div><div class="reward-desc">머리 위에 귀엽게 달아줘요.</div><div class="reward-status" id="statusRibbon"></div><button class="reward-btn" id="btnRibbon" data-action="itemRibbon">60 코인</button></div>
            <div class="reward-card" id="cardHat"><div class="reward-icon">🧢</div><div class="reward-title">탐험가 모자</div><div class="reward-desc">홈지니 머리에 딱 맞게 씌워줘요.</div><div class="reward-status" id="statusHat"></div><button class="reward-btn" id="btnHat" data-action="itemHat">120 코인</button></div>
            <div class="reward-card" id="cardSparkle"><div class="reward-icon">✨</div><div class="reward-title">반짝이 오라</div><div class="reward-desc">홈지니 주변이 반짝여요.</div><div class="reward-status" id="statusSparkle"></div><button class="reward-btn" id="btnSparkle" data-action="itemSparkle">80 코인</button></div>
            <div class="reward-card" id="cardBunny"><div class="reward-icon">🐰</div><div class="reward-title">토끼 귀</div><div class="reward-desc">홈지니 머리에 토끼 귀가 쏙!</div><div class="reward-status" id="statusBunny"></div><button class="reward-btn" id="btnBunny" data-action="itemBunny">90 코인</button></div>
            <div class="reward-card" id="cardCat"><div class="reward-icon">🐱</div><div class="reward-title">고양이 귀</div><div class="reward-desc">새침한 고양이 홈지니로 변신!</div><div class="reward-status" id="statusCat"></div><button class="reward-btn" id="btnCat" data-action="itemCat">70 코인</button></div>
          </div>
        </div>

        <div class="reward-panel hidden" id="rewardCouponsPanel">
          <div class="reward-grid">
            <div class="reward-card coupon-card" id="cardCouponLg5"><div class="reward-icon">🎟</div><div class="reward-title">LG 생활가전 5% 쿠폰</div><div class="reward-desc">LG 생활가전 1개를 구매할 때 사용할 수 있는 기본 할인 쿠폰이에요.</div><div class="coupon-benefit">혜택: 단일 제품 5% 할인</div><div class="reward-status" id="statusCouponLg5"></div><button class="reward-btn" id="btnCouponLg5" data-action="couponLg5">300 코인</button></div>
            <div class="reward-card coupon-card" id="cardCouponCleanKit"><div class="reward-icon">🧹</div><div class="reward-title">홈지니 클린 키트 쿠폰</div><div class="reward-desc">필터, 브러시, 물걸레 패드처럼 자주 바꾸는 소모품을 준비할 때 사용해요.</div><div class="coupon-benefit">혜택: 소모품 키트 구매 할인</div><div class="reward-status" id="statusCouponCleanKit"></div><button class="reward-btn" id="btnCouponCleanKit" data-action="couponCleanKit">180 코인</button></div>
            <div class="reward-card coupon-card" id="cardCouponBatteryCare"><div class="reward-icon">🔋</div><div class="reward-title">배터리 케어 쿠폰</div><div class="reward-desc">홈지니를 오래 쓰기 위해 배터리 점검이나 관리 서비스를 받을 때 사용해요.</div><div class="coupon-benefit">혜택: 배터리 점검/케어 서비스</div><div class="reward-status" id="statusCouponBatteryCare"></div><button class="reward-btn" id="btnCouponBatteryCare" data-action="couponBatteryCare">250 코인</button></div>
            <div class="reward-card coupon-card" id="cardCouponMoveIn"><div class="reward-icon">📺</div><div class="reward-title">제휴 OTT 50% 할인 쿠폰</div><div class="reward-desc">넷플릭스, 디즈니플러스, 유튜브 프리미엄 등 제휴 OTT를 더 가볍게 즐길 수 있어요.</div><div class="coupon-benefit">혜택: 넷플릭스·디즈니+·유튜브 프리미엄 50% 할인</div><div class="reward-status" id="statusCouponMoveIn"></div><button class="reward-btn" id="btnCouponMoveIn" data-action="couponMoveIn">300 코인</button></div>
          </div>
        </div>
      </section>

    </main>

    <div class="modal" id="modal">
      <div class="modal-card">
        <div class="modal-title" id="modalTitle"></div>
        <div class="modal-body" id="modalBody"></div>
        <div class="modal-actions single" id="modalActions">
          <button class="modal-btn modal-secondary" id="modalCancel">취소</button>
          <button class="modal-btn modal-primary" id="modalConfirm">확인</button>
        </div>
      </div>
    </div>
    <div class="toast" id="toast"></div>
  </div>
</div>

<script>
"use strict";

const predictionData = __UI_PREDICTION_DATA__;
const mediaData = __UI_MEDIA_DATA__;
let activeRun = null;
const mappingSteps=[
  {key:'map',label:'집 구조 매핑'},
  {key:'area',label:'구역별 면적 저장'},
  {key:'floor',label:'바닥 타입 인식'},
  {key:'dirt',label:'오염도 기록'},
  {key:'obstacle',label:'장애물 수준 기록'},
  {key:'soc',label:'배터리 사용 기록'}
];

const $=(id)=>document.getElementById(id);
const clamp=(v,min,max)=>Math.min(Math.max(v,min),max);
const fmtSoc=(v)=>Number(v || 0).toFixed(1).replace(/\.0$/,"");
const cleanMinutes=()=>Math.max(0,Math.round(state.soc*.56));
const setHtml=(el,html)=>{if(el&&el.__lastHtml!==html){el.innerHTML=html;el.__lastHtml=html;}};
const esc=(s)=>String(s==null?"":s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");


// ============================================================
// 홈지니 효과음 시스템
// - 전체 사운드 볼륨 강화
// - 청소 중: 부드러운 "위이이잉——" 로봇청소기 모터음
// - 충전 중: 잔잔한 충전 펄스음
// - 청소 완료: 밝은 3음 차임
// - 충전 완료: 부드러운 2음 차임
// - 홈지니 터치: 귀여운 반응음
// ============================================================
let appAudioCtx=null;
let appAudioMaster=null;
let vacuumSound=null;
let chargingSound=null;

// 전체 효과음 출력 배율.
// 기존 대비 2배로 키운 값입니다. 너무 크면 2.5~3.0 정도로 낮춰도 됩니다.
const APP_SOUND_VOLUME=15;

function getAppAudioContext(){
  if(!appAudioCtx){
    const AudioCtx=window.AudioContext||window.webkitAudioContext;
    if(!AudioCtx)return null;
    appAudioCtx=new AudioCtx();
  }
  if(appAudioCtx.state==='suspended'){
    appAudioCtx.resume().catch(()=>{});
  }
  return appAudioCtx;
}

function getAppAudioMaster(ctx){
  if(!ctx)return null;
  if(!appAudioMaster){
    appAudioMaster=ctx.createGain();
    appAudioMaster.gain.value=APP_SOUND_VOLUME;
    appAudioMaster.connect(ctx.destination);
  }
  return appAudioMaster;
}

// 모바일 브라우저 자동재생 제한 대응
function unlockAppAudio(){
  const ctx=getAppAudioContext();
  if(!ctx)return;
  getAppAudioMaster(ctx);
  if(ctx.state==='suspended')ctx.resume().catch(()=>{});
}

// ============================================================
// 청소 중 효과음
// - 사용자가 직접 녹음한 로봇청소기 효과음을 그대로 반복 재생
// - 직접 녹음한 청소음은 기존 대비 절반 볼륨으로 재생
// - 별도 외부 오디오 파일 없이 이 Python 파일 하나만으로 실행되도록 Base64 내장
// ============================================================
const RECORDED_VACUUM_SOUND="data:audio/mpeg;base64,SUQzBAAAAAAAIlRTU0UAAAAOAAADTGF2ZjYxLjcuMTAzAAAAAAAAAAAAAAD/+7QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABJbmZvAAAADwAAAVgAAwhAAAMFCAsOEBMVFxocHyIlJyosLjEzNjk8PkFDRUhKTVBTVVdaXF9hZGdqbG5xc3Z4e36Bg4WIio2PkpWXmpyfoaSmqayusbO2uLu9wMPFyMrNz9LU19rc3+Hk5unr7vHz9vj7/QAAAABMYXZjNjEuMTkAAAAAAAAAAAAAAAAkBgAAAAAAAAMIQKcr0FwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD/+7REAAACYx5TnQxgAGGkKgOnpAAU8WdduZeAApss6zcw8AAAAFK8OBgYGLNEEC3gQAABBOACE67nHd3d3d0RERET+u7u7oiAAAAAhicHwfdghLg+H/gmD4Pn//iAEAxg+D76gxSD4Pg++UBDp/SD4AABMysVkSU5yDj1oWpBNxDyFmmh6vZ4+EZGKxWTo25zz+oICAUIEaMVisVo0e1OewQCgUChj2RisVisn1ACYrJxwIOBA5DGsHwfBA5wfB8P/+oEAQOf8EwfB8/wQBB3xA57AC6hEAwAAMGWSW2797WbIzqyxpnql8GJAPWDh1bGYoBSqiaMAgXNAVbTIuaVxKgnpd286DfNk/0+XtCmd6jW1SKxZ0qaaW4LjdzSsKI3tbudOxVl9lriusR9HarGZzj6mY8yWg3iJyPH8sfDlBtXGsYtb61Eren+7UpF3nx5o1nlsRcSW1Wja9c/mJ8/b5/HjTsd/muNws1rjFvrPxnHtn+v/95uoUcoAhAAAAAAAJUTbkf/h1HFSpDJOllqNkSHQ3CCCP8NKZITA0qvoeMQvg4BczrLicCKRikS6gIAwKwf7hovy4bCVEPS6PVkZjaGFZy8aXjIVC84tjFGjw9B9SJee1z4XbK6juVrxIu/4EBAwMyxMPoP+8wM//0iatr/2p4Nv76jeJG817f+jDFj6rr6/fP542IN/9+m8Yr/jMPW8/eM0/tnOLyxn1LF1dOAQAAAAASYOSQkQQtWAEAbehMYBgp13GUxV2tGAWz/+7RkD4JkCkLU72IAAIULis3sNAAQZSNTrLzPwgavqv2GFxAt8QMTgbFIZslx3CghcahmiAHhyRBQEeJCR5kPgc9AxSJciZB0w1eQEfBXLpuYGR+XlF07/kebmhXLda7oHki6+tevW9tUwZB3Tr60VVsmZvUeJVzdA3Qd0jYsKB0+llvd+ndAAAAAABGz5JI1YIuNxXaYmN0a45jgQU9a/mjCIjqiDAOMLiOcOYOQcbAPQK6DAJ2FWH4AOITIplwe5fG4eZUTTpMOE82cdpCHmPAvGQwon5QQYqGFNiaPyjckjA1PmxRM2X3QOGR9PR/d3//////7My3WyDarfUuv+9q0tV6ClqUbvLpvwRAIBZdZ4Ukp+AZwhAMsxBGPpPO0q2/1Qqpp/vSX6epOHMeEEfZbqtxHusM7E2kQSFRHq1NCmi9nbynJmaSWONcKt9FtW6uhsikbP///ATjHRuxrPz+dGpoM2P8zwiWXHs8OCCV6ivG31RH9zvjphA5zGG01Jo038vV2MoxzGcn8pdKsAiTH0t1CM3lfpCe+gF2m9AzqJFwSFkMKQQLbWuwZiC3pe/kcR5SrTPXo2iaS8Eyk0VlvY/TO2tKcTtqCY7AseHlU54LQcAgSDMQHVJL8dT9e7x8nH4uUXcZTszhWQBBEfp3mTfr/////6IyleVGe1vTp+RLRzsWPnSNYQU8hBw+6gAAAABT4jECAYJAoASOZQsIPQKdbAw9hrMlMpUoXDr8tcgRl89GLy3qjvOZivt//+7RkGAJkUUrUYys2sI5L+q1kSfYQ+S1X7D0twh0wKrWHntBaNCxQKw3KJSFsO7s+7L6OYgHlUDRCUb/bVR9kVD8NBz/9InBqRD5PZ/5gfDZYhETl0anaebvUTrqCs4ky7//7/0bp3BAscix5KGuTvhdj6gkG7NhiBJtxj/e/AAAAAAAQ55LJn/p2e0j7AWheqyk4UjnMd1WJiJEWqkJDpnrsis4ypnCpUeYQka7T6raAI7QnpfV+UrV1w+xNrVO7MFxZ/JTH5A0FkKm0nlLg4wiJ08++01DtWAMY/GXYhuMzPP/9D9iYn5Tu///////aysDQ7o9zj+lFK/Z7+JfPJ5HKG5N0B1NStqYvtMYKIgAAmthC0LAiSHqNKE5nB5GjUjmvZu7RgjwlUvaynk8P1HSpAZsFVnIlFeYZ1IeCeJiLolXKsm81dF1BDg1T6njw9//si8ZDksTf//2GBUwxrf//oniblZ9aFPuEY4SpUxpL6KRn///9/ucemirVTToLrRrZ3VuRRRg4skk7onyA2psr9OhBIAXlDFdzdND6hh+ulA1pAG0pfhiKhKSNDpmUooUBSZSxJrLOgx6CwCCuVkEoIsJniABEuBR4YnTCQoui7QL9MmGqWVqTyHGKuHcVWmGKYeL9DjFVUJmJkBYBMBhZQkJ32PQiQKv/1W7f/////9VoYkzRP9P9btNjVg6jlGKGicamOYhg4ep1BMAAAAAIwJaCTS3jKFUtAwizza2TiUJLWswTvV2Zwy00DW//+7RkEgYkOUrUay8z8IZLCs9hhbZQUR9RjL0WggKl6vWWCxBQ8Mp49OwoXhzmq6FsEhLmvmAH0WISzVbe81wP4DCEwsJVDyVQ5/tqVPYTsNKP//8aT0BCqRJt/GviwY+JLxmiqjEwyxDmBK0hhiH//OfX12nbsSZ+gUbOX4fecoeEpL5H8SdLOAoIAAAABKbtbUjMwQnvB8yd4IElbmvMKbZeKIxQyKLGbEii+LXF/xtR1fCc7FlcsjWqrQpbDcWUWA8XgrC66EpKrj7VE5FRj7CYEIJ1SJDD0iGBsZl5iI3bRFVE8xMzYpEHio/f1kV6l/////+hiEFx4iLi6rnBCt9C1/+ivFdc/pvUoTIQKpANBY0h80dHoSMaUZuqBy/2nCw4yWzsQ0MGMMlt2YtfdN/FAU0GOuw5L1NH43OXAAZphcNetlYnNf6MMTRwNs8MolQO/tqc1laLxETf//FwAp0DBzUkSHaHIrVVXrUPJ4ilHjYh0S4+0QbMlVU8pjZFRBJGufMV8TIsHoJFDy0qpQGAACndnjymUTSM6dgqe6OqqQkEKBMOHAxpwIoX+sZVJPx85InW8DuoD2xBiSdqPa8HdQvUGZY5cjXs4cK45OA7tN8QhKAeECCSVgAQIn1R4EkfAJrrHqwoLG72hizJ4BMdGPXb7oYTb/////0bMFKxlK8Gph4g9HPgOFx70yjKiIQAAAAMoW5f9ORTVHhs8bJMGHKmaC/jRx5Ay6ipISxBQRAFWhwQILgRBHIouZr/+7RkF4ZkSEXUYy9LcIrraoprAowQrTdXrL0tghSvqqmnlqBg+BtqwGcXCAGeWJOQ/+kitBWj8RwdR0qs5qNjhVbQhFGdJG//9jDzCs3fZas06Yqcz8z3PIwnlUs5pCwu0y6FR+R29UhHbQaHQ+gaMZEUl729il2waBIlL5XAAAAAAABf13LNnpec75BHcBC3OMGHQ6GJDAxeaoYZFgYEMBUgQXZc0AsqBRvsmcWjSWL4HR6X2ZlMNqS9Wsl8vFOZnig83p+0dWOvTSTboF/UH16z672qK9jDwvs0yclcOyfqXkqhmjlFJdt5/9YtyjJZpXbvIyf/////+/9d+f//ibjvcQjDj2wLNgCm4E0wcAIwGrByRoAPqFIV7waxuTlhkugISgrEQUUUdLuCoU6RKlMZLJQgQ6HM4hji6N0NXN7n/CPYnhcVE4Poa+86qZKJHhBHv//+nCqUEe//9GSFkcqlsP37rLEyJFViph5rO7/+co5key4shFQrLG4LPR7vU1aCwYNrI8Tz+4f/9IkIED//O0L/l/AGEXSgquhMMZOK/GD46DMeBMKLSqCFUAO+ECkOagpAHoF5lswASFdbCfCNFCRZPxbh5jhaYzcqi2JGIwsJuGAUwD0dSydJDUezktZlCYm1a5ro315cK+Myb//qY4quWStdpV//////6v/t///RBaocMrB4ckejCIbUVNL1vgZQIAAATcypRNKgAVaAArFboc7RNFBtGYp6twUCAlVCSwqjLVXSSsSq7cX/+7RkFgJkDUtWaw8zcIwLuopp5bYQSR9VrL1tggAV6eWsrbjNRl/JizmWSglz2CqYtP+xCmKNcVfPK4Z67gtqXb48+v4/RJrJnnf/vZaRhik3FtST+d7UffPlmyu+d7ZKWvE6MQRMCULRXL76ZK1lJWj3236PHJR/QaIAAAAAAlzC3dpo6FQx0T7IE/h4G5YCANHGEqagWMmXAhcK0gtoFgSBqu0kFKlAQqHFmQVWEwILFWZAoqkcrob6FH0LCk4RZtIfzW4IVko0ONYykmfgCuVY14KnJQvkuZWhjP0uTbEiJ3NN//AUNFhBjDjaaleX//////1T/t5v/6VUk7H3ePdB7NyFhBAAARLgjCVy+peKymu4JwMq0xx3XcUBWDWWDpIsXsRZcqh+E1WUyPxdLoMVvJOToF2O57GXb7/yqMH+GGnprJx9hWXCQ8QNQRJ9+pxJASTi05f7SdWda67KLmvUYrnIncyLeyJ+Xcozdw+yCcaWjL6Ktf+2QTy8thYFRQDhs+7/0wAAHlObuzDstAOceEJAYLpGDAQttIQaNEwjWJlCc6FyiC3zPBhRaIUQCHAdaNUJqBrJModQhZ4eVKB1Hl6tIRqmaztxSNq7g6csu+7dODpXvT1bizl4WZl5kvWZztsxD+A5OgTFDxQPHF//QMzFY/pJ+7//+zpr/5tBNZFrxhvatIhAAAAACDwyKlrDYEKRYdJwD/KRPSSWJNr5iBBOiS0Re7GFBsppRdHOKthdlrcFI2wc6KoSIhr/+7RkHAJkfktU6y9OgIzLyp1l5dJQYR9TjT0Wihcvqv2WF0h8CO207P/3QLJBpb7NUibv0E9Yp/+ogtCOUT+J/uUQiZVRY9k5/V1iZzP+N7//WZbDaZSE9ii6lzqCvt15fdEmHqiUWjBrX+o/ZYI2DacagnAkbD5v/J55tiAAAAAAADVIcqwC4TvioRw7ygu6wAgMWsX/SOOkBcQOlJFToFTUX2FAlir5R+LOBiQICR/BVLeiNERsrWZw/0IUXRTgDsho4i58vjbtv24zdyJJBMY9AOYvCbL4KEpzuaXz1Hl4Ud7zSy2v+7qLo7xEr+Tstmo//////p/r///0ysERScKIRjDzHFlDaCAgApDoIlopmNBFUCKDWhC41VVpEVxoAsjEClZyir7M3cONxxC9EJ1G4NopJ1aJYN+xGACBTlq3nKFhE3/Q62gRQIeTqBHSev/dIpclC1jX/8BxiOUL1FMw4XMFBouZMp/xtN1Y8p6Z8nr+XYpjHWDoLOmj1Qdd9dOHIZUVvhdDUPSVAQIY8ARVL0KHtqsRQ8AQJou2nwm+pMqnBVQafSEYsiwJAMVgtCFgaSy3CoQwxLuImKSgRdYZEcBkUugRCe3BuMTkD8xhsUKoKKw7TMXUIjIjYQi+PAer1DxMlwsplNW1MfUmSitxyoQ7vL3//////+r/+////QWmFykQPHIH2EgtyiIxql2OAAAACkI3vOFwpigq+hUCy044FCYHF2nLLJQC6gCvQrbd4K7P10dXARQSFVX/+7RkFwZkT0vU41gzcImLqr9hh8IQpSlXrL1tggsuKz2HitmT3k8++C2krlaxhqTqLTI1T5f+n7kwgkpm0p6YxLLPf/cTicCu/Kp////mEwRAjaGet4I4dDCelv+/93NFGxorD9vzvxc3fw3JOlB3mmJLLbWq8TTPTF70scspUPzggAAAAAARL6g6zFFwmKgBd2TmL4eBIUvOwBAekIaPB0toJ1FEUEA79sGhYlxVUHqVi2oKjirCkcLLSXbNca02J1YkvORUwPI0ScrHoXGJLGycQTsqnTJJMSo8I5AuBQD7nkXIJjZxaDk5Haehn+j3/////9XVGJtTORsx///RpqHcdLOxUlPSkzESSnGCwxttTRbSvBUcCnMwgaKBqqp0pGF3jJFDeEwQhVnkkcoJGgISSEtFalwZL1cHdCLchwpVf+3IcaxclpMLDhSV/yxhwVaN/+4lw873X6o7CQ90lVNvf+hTali0KqJMRb1M6jpiUamR2ktKUmKxVLn4Pw00BOOuPWwlrGqRINn/+XLRAhJD8dxGqjM7kdgs22KGsqfFSSX6agEUl0mE2sJHmw5DicK+kq4mo8tNDQRiY0hCiyqFWlS0+m0uTG/MGWWHBV76Y/2Idokh9QEqlWVjlfIu13qEpN8tubjjUTNN8KKUIII5Ec6/9kL/////9QhVterGd1v//8IQgRldAhGQK7msqldQkQAAAAAOTdbKlBfcwJDIhB6I3nTCTLh54G7LiWSVnZ9dgnUiuzDM86k87cn/+7RkFwZj8UtXewhN0ItsCr9l5bYRcTdRrWFrwhewK3WXlmjhuGZTIYBcF6CwCV/B+CgFyQRUinrSQeNv/83k//8lQ4BsPYt29J1opnknKtHKuvjUplUR43kWUOlOqVeJ+9L2ZksDqrSP6TWtj5AcQjv6ykOIAAAAAAAAE+nYLBuJAL9Ouo4cjq1WbKclgVkJWMMXAQcdfLsiqkvWqmA098FGWYaViZEn8sh/BIR72XpMlKlGJ8Lcp2prUjyJMpm1rKUZK7YBE7u10gUluJFfOSoVMSG3ONr23vkCxEe7L6P/3/////6tQSHK9Gtzy+//vcwopxU6TIKiQqNRpVjKQGCQYXgDgLR0OxIBXTVNdMCBas6uWxp3jsAtQH+D2uZALb/dECQ6amlmo7rXaB9WKM1Ys7WqBCbUz/5tRNRy8hax6L0k5FId8ll4bh9PjrM//YN9EUd3/8lbHLvRMOM9E7mH1UXONSQgytWKqauqlt8qtKiPRLKYLyYxd8HjqkiOzL2x/8L/K6lfmu0IWnPbVryq2IIl5xjA5ldr3tFa5DIjELyqmZ0wJPhiDWVZGFlYpYyVEBBSh5eFgTpJC2R2sf4/2t6u3BQNzdLNm65QY6p1emd22fBoKND4qjWFQ3McZac8f7/Dw1Q+JjxYPNHDX/7P/////rZEBRNDtpZU1EGU9e/R0kHIK5inIplfRJw5eHAjARAAABK7i9zXFhzAJCSDj0AVijHJoU9dRqRfRm8vqPAYiThWOhJmexKyuHz/+7RkF4JjzkhX+wxD0JKryr9l5bZQpSdVrL0PggUvK3WXnikLSYeUHq3zOmBKGsQ7bONvfVh5Llf/2iyv/+HNCVXKPmOFLLIGBwc0U9DDkHcf69tItyw4UD55OYaNHj7mUWgFRIqD6DBUY1JhX6JWQIAAAAAAJN5CQCirkAiJhAA7Y3yEAuU6SJjgCwqzyJwt6SApiiR4kGlcJAQ+BmSIxZ7oUbzQWLBAYdjzyrPmCCkLElMpLP3jU/pWqlXJIh+oSkTmZzEal4/z7MBWHisvIO4bG2Tf/8pRpTRcrHM/MxuRVqzf///+qOQaGOI3/7FoQ3o34myHUejCiChiuc48N30xACAEi4IgxI+FJSLVLPOSBMhgRS1ikUTGSOIRFlJDvyOU6HOGDQFYHrKLdYPhsBzDiRIM7SGIRCn8PUy6bS+IfPP2Zl8iswabCaSV//5IcifG1/yh5QdDoGwqj1dWPFH2kpUlIHx/5FRKVuUYWLEijJIetJzPWSDcKLj7x2IRGPVMbf6/cGElOwpZmDptKS7loSkZoDSFsJ2I+umVgFwERH/RecOMI8N4aAN1kJ6lQuTFHaSQEsLWUBemxCy5BtN0VwjruCmtXtOslxTakDkaUvIMMW5LxKEiznFgfyhu3lS7PdkVWx1TdVb2/////uOGuuj1O/PT6r+OrR9WYDyASC+5Amx1vQYAAAAARL5UAErlSihah6PDgkEah8ohbN4FSeHDB3EKVJQH8m24b41iXsr911O8TR1CWV5kLy//+7RkHAJjsUdWay8rcIIrit9l5bZO0S9brDUXAgEuq32XntDbflOjB3HUgIym+dY/R6uODRszf/oo1mb1kMECjRv0QgqQp0YybO6/Kt6NOgHMYaVBdQ8d5qECzIKRHnv/9CaQAYAAAAAEqvHIS5aG0JlzWAegkC5ktUPZYg2ourCkq/QqS0eQQ2qRmCp1jqKsHWBKggMCZS1B9niZK2ixuI34DU9OKJCc81gIo70/Z2I2MI1Xbgc8CrgyqFmRzxbjtU9sf+gRQMRzqztuRr//////6IykRf/7//7t53oYBAILYS7uYxAQCjtjxEpCQYnD1pE/gJ4PHfBijZWqKeS0UsczkRm5VNsiZxOfUvbja3XdgiDrLymxJPrOGw4BTMkCm3x6FYwgldf9k3QMKOimo8f/+kfEEyJEAoXKWHb/nlI4WixUGjBdRQi5UZaDYhJFAQDtOG9Md9X/vsSARST4NEEnPoJ13WtAMd3GWqDKmaO36SqWqC8PoLN0b2JEAMHppNiYDLF1igk24RfmJu08zg0KNKKuE/dns+gXaqJqIj3KGMU+TFWmZhc3sIZAoGheJhcTNsQ6ux5GS0Yx7HqY8z//////dGUl/r//m+mpyEXiOOCOFREYC9IZnIB1IBAAQDNOI4L7LAjnpcAOtYCwRoSylMxEFfUSdIWE26eBRQISZD6qAhDw4QgaBDd//yJum2Hp7DP/qIefHf//7Yenu59+uUSQbmV/r/0eIUSPkC6p5fEzX9fo5+VV/ackBjL/+7RkMoBjt0lY+wxLIHYriw9hgrZOxSth7KE3Qcev67WXlmBNvYxm93w1JxkkFyC0tAZKax9QwQQAAAAAEnfFIAzeJsiVchNRmVAJ6lrMHTiabaqrOGdMQcNyn6VF7TWXcdB2JcoArG7dNTyJgeR+IpOxuD9q83JLjYU3GYlEZGNSUzL0f0Li1JHmw7MzLqwo/pXU99//////9ERSMa63/6f/9H1CgnASq+KnuWBBAQAAABHMBgE6BlPDCRaAIAumOItxx3Ylk08KwbLKd+b2dLpqTQp6arX5t06lWgvRaGBHj96cCIgDWTF6/KoJCgk/9a3taX4jKQGki6PaES3qor3rbpHK//Nxd1uWqfoDMidJQ80a2WfNXHB1gwnkq6T39HlCBQfi2PytnbY4kZ8bBlh1x0sdY03jN06UGmtvAkFOosvK1wTUD8ymMGIEEFuWdFkyqFaUysPJk3l/IzxasbZGPxZdCdGrCuj0qqmF2MEgOBCiwkHiP8ciMjcn+v//////QlJvL/7f/9X7uDilnI6C5rYKEAAAF+JoFsacCtCp0PZaeohlasboIDckVGoY+XI/IMYiuSSRCyZg7AqYKXBDClsUbdYo4hACoPYnhv3toRVrYGnf+hDOVxUjP1spZRpRTc8kq/9Wk51Vjmr/r+/579utrVCElHYJEm807+CvyJkItV6emECAAAACAO9MK/GCXroDNpMFra6W1a85TPi27dnobQWGnXHlB7SmTbuUny5CZME+2McR7m8aKSP/+7RkVgIjnEXW4wxMkHaMCu1h56gOXRlZjLEWgdauqymXitm9KP3HTxtjvollyQSdRwGZCU9CmB8tWn0Z2dykfw6b1F39foo6SL0n/s////////////+r89NVD7DiMRaxZHKIQAA1CsyTDlFtwqGhDDx0iDw1K7Cw9MwFZdC8j/SCZl0oSpo4Dqv3VqKAKjfit1l0YfQDyPsWsAuCYh9WBn9jmCN5EGp38zCiPY0ktIMfTyZD/qPmv4ieJ95m5ev+rvuSKY8gMg1HBaHWH7Pl9hd1bdSxgAAA2Y7+UbYO/QhvDh0xmp3J9Ix/wuHJFKUz2+pHhTmnkBqhrQ35cQqMgqJMOTsJdyhPwujpTH4jHJWJ9C2RwgrAyFeX/Dg/UjMpAqCaH9KhL9iiOSnrrE8mb47AoljHdl/aq//////+/enr///Xv+VMDzC1RzGTEAAAABZMGNKapgILKUlBGOCcUN0hH1T1jbYkt4jL861rd1XTOI5dkXMlEgGINdJssdc3nSMgeVNtpUY9785hULLV/b331Ux8YZDgOgDDutCa/cY9Ssqek1m/8Xbf5iDRwDiT4UVU7M0p5kOhSnE5VI0ilPRjY4EiAAAAG1vbx7coZbHhWiSsOK8U2ZzDbJFhnV411pMaf5WF3tOm0CAG5UoAzIDg8HweOEYHz887rQj3D7EB8hm+RKnzQwM1xcUrmKA9Epy+xycUoFxmyGnI/+n//////U02eldCzp70W2n3vZdpqIhg8QEkSrS4EZAAAAD/+7RkeoAjwktX+wlFMHXrqv1hh6ZPBStf7D0Hwdguq/WGHtElJuvItksGGGXYHTpA85L146kmKab4Mkk1MpFt+hqBUKdvplfQ4sz8ZEqv9im0xgPgIA8AYRoNqvjKEQNBZSrzBdJQUv//4kwdHz/8V8cwt6lrf8KQNPXHC7li8DjhWR92cqwj04RCgiUi3vBKimQ/+jVCMAAQSd4b1Srk8MqBEy5DkJ6xVrEVVQctYzWFgow+stULaEiy40JgBvkPC6SSDOoLpIOcQOPiFWdiQ2qs2P0M5bjgMnPBUiLHTIdCglC4TGMqc2WG5YNi0wi7X57///////Y2Yh7G/f///2f3Uuo4QMH1FnbV0ovAIAAASM7dFA4fLtp8JSMhE0IXMMRZbsjwkw4aTbaVVQisvg0npOF9NYcDZGZELa5khZPDj+zRGbRFDAcWTbqDr+wsRYXS72ucTkGL//ArmCrfd1HNr7VtaMnF18Q9POnEB2JaqWNul43qJFQVAByol+3+XJPTgRgAAAAAIA1yXvyXZZMmRFDb4vFDjkN0QzXUKCSpTWXYztVWTOSUEbmkE/qYtplqhgkGLolwE0+BGCWQALCZFWxcHyHyofnxUOKsC8lOQDjGevocCUvMHaV7vmemUKGClUn////////////+nr/mYMil11rbAoAANO90wUpnoQkqBEpR4IPYZ0/kFRJsD7Kbt5LrkY5Mt0TUa7jRZRlpcCQO9z0Q9HxWBQ6otOKAWBo1EQWlX/ME/+hQHpb/+7RkmgJjtUXW6w9D0HVrau9hgrZO6SNdrBzWwc0t672En0kv+URJsigShFqn+Z/+N60TbfN7dvmvEx2BSQa5NKR6vGlu7AkU4UmzhGF5Iaj/xRCkCJBT1Oa1LQQOJG5b6MbcROFXcrT0agmez20ovdnEq3PCELknok46+o6xJckMz8igaZeV4XAszV3uVNaz1FGByKZXDgMLFnROheKs2Tg4+O5//Go+OuNlMSrf//////97T56He6f7f3vXrqh4cXFGuOAFinBREhMAABK8CQpZARjTEWDLWRtExVnUeNhhLkKIetOFxbZLtgEyI0JbGvHTJc1GhKFMVoPrklhKA9kONMv/WDSRb//hBav+PEg0VKFdrq0T5q4tjEIIcZezcjC01dLpmcXkggIjbiT51iVCzwUIuHgAJ4iIaHwAAAABAWzz1v7bSzqZosRTAdlGlpFpDRiYgEeHTyfCFG4OUhiFFzXQrqtVwQFOJyRdlgN0ukNjcGZqqxu5n5+ItVtZvolmLazLsqH0GCwynPZ1D3i38nw4hAYjL////////6OhFb1///7UL8MAKZ080HfBCCAElAku7qgouBAQLEZSFRtq6D3tsiYr4hFDcXeKU00/m1J6HajHKfj+v268jdmNt5G/dSoVSQCYSiw+JOo+QVhaE3+5OFyYZ0uVBkpco/cjP210FPvpNsym7/8v9sn2UJJ0zh5W9Vv+thlIBIyGBZS9k9AQAflMH0zs2ow1w6BWhK2msLXOyVVNGhgLK0H/+7RkvIJjsEhYew9B8HJsCuph4n4OgR1drCjWwcquK7WGCxHkKXvZwlA5TZJxt3cZKSFLqsEZw6cGQTeeZk8zMXsbi8/UNL6NkwrIaYCzb0a6oEn4rvcdL6WxzbdMqjkU7/////////Yl/vbr//Sc4vVEQpgsO0uUnJ2AQCAAAElO00rEFFpFukDjTAiAzeWUryNcjaCJWCvHH2mO4LVpFGakjnesIkVM11JO/EY8bniUYPAGwXSg9LtqWYfMTv+045HP6pg5gUiGInZO5jdpV/3YwzP//2ps/rH0ohVmnIpORBmmspisNrDOLCNEihSPiZ5ABEAAAAABAHZXAUNMt+y9R9A3zBHQeZab8JS073IZqVxOGIiLCcJyYBiz0xdeLA1il52kMkh4fDdGV15N5weW1X1jgLUZwcrXBoOzFKbnxWdaMk2vW2LtmccODA2Yn+////////////2zrBfnAdUp1imQgAAACLTIioOlRwQAJVIbCqosi+6GyWJV3Z8OqC2iElM4dNGgYCaUPDizCISLq1o1FxUxeq1giJOAWVURpHBq//x1yAoELJpWN2UEf59Zf34TTeRzQp0v//+xKh8ZF2ly39wIiGiXZtQWR4+UWU2Xwu7mhOf///ppz6mJJwmmAGbZw+F10JZqW03jaJ/Rq+ulPZuvpAl5WWQAEE+OCtQxjwJDAoTyh9IWCRgFASIkGnMGHT03UOQADALw8EECRNXi7kz4ymxD6a6CRa7KYUouzF+khBB4QDsiqD3/+7Rk4wJjwkhW6wo1sHLKyu9hgrZS6TVNbL06SjUvKv2WFtkOD4GvJVI0DFMTicVDINjAOAMBG7AtMXT84esc70zMhwVEwoOgpV6SkEa///////MzlMbzzNlF57P8dsaIndFOpEFR4uYpwU8VlegAQAAAQIPEI7WittgBAmNRGWchu96lSyxGAmQsUJEL2lB0CLngaSjJAFJlUFxSPXIKDAU82RBCTD26ddbLfcNwIDQlsNObky3OUwf38r8OwDSqPVP/5ndXipLGcM+35efXlMSNRz6hyDawYicLIVKJOiv/+EvYx7ugYGsdIhA3YQmXlz3JuREacPDnR3MQCAAAAAAFI+bfA3BZdvFNRMMBrl9Y496vHyeccRCFwowPAuyrhU6wAOBWoqo9hEI36YQ4ZIhYwWRScTCRIdd9W0cimrWeyJ+KDOpuSNqzcpieOAe6lAnGJ5XHNOTzIBsZ2p5535nDFDgqYXYb7RMggCC4gEn/////+/Vf/5ke//NvYDgGYSVBwaPDoiww49N2BAQAUbnbAIUEgVapgt6GVcqkjDkNfQEK4Q/BKPjsQpDp9DBDiVSPHhCbzBHyyzEpPNDZZv6P/GChwiSrdNv43/KRByI1X///6MXMa/4hADGYhkzvyvrJbhSWWWq+3//n797OXyRCXZV0+Mzm08DMTGvpcNl6UFP0dABFBdxG8x7qRNKB5BCJoUqY2IRu2XNGnv4upaLJXJgxUUMtWRsX66qsywToC0FWoC7jluPF3ycCPv3/+7Rk6QRkaUdT2yxHEJCr6r9lhdIPLSNbrDzNgd+vK3WEn0jKL8poIzfp+x5qM+XBQCAyJi4jNME59iZlZDj4Jtf/uOCgMkTq/5vNf//////9Pf/p//VzFNIs8W5qEBJPmIAAAAAACThUBDphEQFixgAKAloAqQm7ttWnI5joQzeRIP805pcGOI76sU6sK/iIta7JaEqAlzCQZNBxnldd8uV0si2hkqpQ0mV2X87LA4BkqcHP//yixh8TGf/zk41cmZ+cc3xtgqsmlMUSWxEz/+nn8J4NKSgTgwfZRFkjxGdX1eL2UwXjCCbDWWaW/YC/72sAAQAAAAABF8sDA4suAt/NqKQwLXGsSAP23VoR1IkCctJcqvpUNJEn0/hYCUKroDED11ByiUK9Uth5BYjst0aez1ej5RijgSRxLNwK0hsOQvAmEZs81MtKHX5T/baK3qH3wXWEUk6w+38zgYFjwUUGhn+rvl/////+k6mbQdxDX6GUn/lUPFIpjTCZQQeEhpREURs2kGCHZuQhjKVRQxN5fzX04VdMvdFy2crqGArlkQk9kxDesqXnkl1s9XNOQDtOtGrEDfg6wehQOmWz/uH0PyGB8uBF//hVW1/5OHB4F2k6YdkrxsjXxtiELE2tv/dcT8JdhwYIQdmBwskltCiQRxjzqolHTGKwJtZAzT1qrAAID7xLWsX90qZIK4yGVypdRe5aIoJUTI07BgI4N2oxLU0SwyAV5hhFBxihERDqBXDeXadOU/jmtD8FexH/+7Rk74RkiEpU6y9NkJNr2q9lheAPlStfrD0NgeEvK3WHljDeTrgo0Qq46nu2XYypVzPAbnkeVHqm0+Jrf/h8aInMOOzz/f//////+VtE1X/1L9KNrJvRRykJlCEHFdIAQAACAEyqFFsVXsIQDICUSpE3F2P86aViSaP4qtON/Hfc5lDUqajU3gas43MmsQfCahCJDWH01l54ET0BvnUmVh4jVDhnd9qQtERie3///Pkvppf58AzVIIGTbGdX/g88Z3LkTmKMb/58bPfm5hM4mbZx5T7LVs5OlaSAyf9f8AAAAAACafLAEzpQz2KsMgA1jZKLPXetcvMXQBDIs8AmEcSDWr1hTN2gL3Ch1xLrcgqJYkXyDhArDgyEuaCMUGOvnE5H8dq4YKRm8S5poQ4KxRLSEtgcCU2dGLumAnr2FGgOP//DqhENHh51HjK/+lX/////s6rK8ipQ7/5m+amRw6gkZKDTiUNKVBuYSUQAAABBXbIiyvst2ouPjr/fFrSCscfJK8aGAx4dfAy/0JtA2j80YUAaBKZTuYUMhqIJjgg1pLKLMASzkek2EFhYVVjddsvi8WzwjZs6JGuCZOX//4l7bX9UnaZiNkeihf+d5+J/MetNRec///8IsITujwuQRYtWqC1ad85yHdfn7cHd23q8k/CAAAFRmdWYxhwc/BjXUrTyUFhSqEWzLQkThaQALAYgEAGoQasip0BamaVoce4SWKXSwcADo4kOWvFHkEzF1qsohKXKSDEmzyuJy3L/+7Rk8IRj/UdV6w81oI4sCr1h5bYQ3S1TrLzaAjcwKn2Xl0iD6dto5AUFFAqjCmEYIKoo5ltjEhRvRDPE2Ti3AV0b6//xxVAcc5f/61/////9F61aUjl/b69D8xlYjZbmEaHqokqnMgUAAAAACJmHIgAGMxNGLEIkOTEBYSBiQdfasaHNmrJ2LiyZLsmBJoNjopXcQEwfAsPZzSqCWjupPmEEKoPDgp1IfuUX4oTH3lEBxOR9yxP1pBA0Um//q1z9T06aYeJY9qybGJX9vbCxpa+25uKas//70iaqHmqrhBkFElOZXhncBqc6jwdvpo/nWWfdeGAAAAAAAABPGhafQasJlKFUBQ4u0Zq5lnixLAC4qxVlAyYxhjMMGiDVdEZVVN5HF6JCOnpWMCaSMnDgDAxgQ5AXyaecq+D/HzYrzGbRcFUwPSZnIXZOARUKTZakKNXB2i8S7atEO6wxLUKLRt//6GDoYdzvvoZ9Kt/////R3KHnlkQ5qE537Kv3uqbmDg7MJqOkzS43GUH8E1SSgIABke5UwGUEwQCG+KGymCIK9HvhdpkcYWQX6h+Lx+X2bM5clFrf6lzKbLgpzvzSdLfbvFECE9LB9a2GaVpyHS///1iZJ3//Zc2OR0vD2P2CmoUgBU7LSi8///9ob36Fytbme9PTML3M22IhayKhCUoFfT6q15pAAJt8ZKnSJA6AqGNM7c0ABEJS7GvsWLqOeOhkgV4FrlmQYyqlTyd9GtWFamKrhwoIQCvHhEYaVTL/+7Rk7QRkb0rVe0s2oJpLyp9l57ZO+SVf7KTWQhIvq32mFtkPNmw0G6xxsyLEaJEJw6D0pjREwKj+SgQ0Jy1uPkpSY12v7MyVRMcICZcfRkWdx7E//////2LZdvt//1uRzThBLoLMLocKF2cgvLVYAEAAAAAIyz4sex4AkI+o0MGHDECMWZjI2gGuiYMSMYjBUIbWDndklG9RQTe+PPIQgkwlVQRgrR54cyws5l0vhOBMaBssHwa1i9O5cxiYaUr5mfyQ+AWOILdPi80RtFu4a5vVxFZSkDMpP//N0buikEHsUJRERpNFGflyECA8ywti5t3yZ6idGJzVH4AAAAAABcnS8E5VwNh666e4JTDHWGs4QBQEaASb5EqWkOFJCpXShcFo+LbYY9pfktxbAKACdQQF5RgNqEFIgyE2E+yzQjgSZyKxkyXa5fGVpOYkel6IK9AyytcJvMJyYo399xv8CYqNOIizurfQtWe3/////oUwTlYQM50bZNOvvzIMQTQVYPxBFEDLlUw4QVhjNhCAMb3Q6n1S+hCKCAcEHMEcRCwvzB7qJ+rsQ7CAEi4ULLJoxUazfTAHxHIgNADlM+eND/bShnAXkUCq9+GrFGuzxzHt//Iw+BAR5/iA5FBw1Tf9FgYtSs0M1v//765NmCjyBFILdVzb8ihkgLB4LhPRQy7HFjvHehKK4NAMCC+Oozv0MCpIw8IjF/mrp7wMIQKSWWsUvmjODRx+OujAbR10OI/ajzBRYYoZekVTGbjBGnL/+7Rk6IRkW0xVayxFoJEr6r1l5bZPmSlf7DENgd8vq72GCtiQHD06OHC/Ut2aMi22fmVDIfyLyGZoZXTtl+/Lm5ldMzOmsEAGZMn///////7od5U67/7ffhUBIeGoNRGqdTMDehMgAAAAAZsK1nSaNYseYsPPjJo7coqVA3YflL0OKFRICVK9qY8apJUsa7GIZf9+cGygYNjkTEiGXS9PjjSqo/bVLEWCVEWzQVcs5zuI3FzOkiHHX//5SK5/9/ymIJsEVeUP/vmqu68hhtgxJj/+vc5wyoOwuZIDhO0jRIxgkhnq5QMQFZFQ7Pf6lwBIAAAAAAEFZFx8gIMiLUYyqUZ5bkKCAI8aEX+IC0OJlIjQK8g0iDGIs7Wo0AYHZTOFEY8eI1UQF9iRRInCWITsDOYAkarqPZOog52E/IqLU44hcGaZNMZxMANpwTiHqS7mrCsetmlLTV9fDsMBCjuvy3/////6P76vXulPk1v80jvZBga2yhhBkaihRUGC0UhohAAA2rwY2DUkSTqRWSYAbIAIO8SBFHNVVW0i4WFIQ9Uah3WisQuM4rlnwiEQzsZXqzLWhitcf4DiuiHYaPAfOGsViWaSHCf93PfWx4/cSyjshv2Qbk9CMqUt/LFTrnrQahgel1G44FiKsz1QeGg6DRZ4xMq4DEfuUyLcCRoPjKjydnpVFQCFjfErFIDRH0LUtnK3u808toLAQWgtd0UYzIHcY6/qdTogh4XOn09yaUtfGLOm4TbPfnJ4PmH+v0X/+7Rk7gJkUkZVcy9NoJAsCq9l5cQPfRtd7LztghIwK32Dj6AslMpX/LIxmztl8zGaFmmopmAaJhgCo848LizLxS4+IpNX/5R//////f+7u3/6N/8ziwG0lFWotcABuIAbVAVVUpIBAAAACZlbgHeqYl7CyhewtiavwXDNmZ4mYs6LA8gVw7aMxdmCSEW8sKuSeV6YKIRpDicEgLy0zJp1u+FMZqsHoG+g8vlfAde0JEgk0l//0lZxnPqqruPGpvxf/us0N9CDVNjS1X97aUptNvY86oWLHipI0YYFbG93vFI0Jhi9IobM8w3greGv31CgRgAAAAALM4jROdxzGHPsqrKRiElPQTQMW7TBLiIpx8kCVXEYqnbdZI9DrDR6u3mDjSsVGcmadNAtWd15SdbGbh3RXFsboJOUHjUVEC6DwWkSiRLJp8xyopUssxyL6anjQYD/5/w7lTjCB3/Tompjf///3+sweMkDSz+ZqTba21tDmKIeh1iQ3aOD4Eo2hDaSQAAEAqImkraACEJTNxds+vw4CAGp0JdQ0FASaJMkAi3xZzIUCJCqHyDlP54T8ogJIIYBqBxCLJG2B/LGUnOvnUK+D4eGOo3jCxJXciMa0gjUL1//0jiRv/JposNLDqb099FD77mbPizv/up7akRmcQosRR2YPD84dDs04TjaFWJTJLCw+ijU/9iJhnkJ6YLY3TssklYBgMlQEhK2qMhcESmBRoCCDBzMBLgLDsHeFOVmcWWjGWdhBJYEZgjyWiT/+7Rk7oJkX03V+y9b0JCLqs9l57ZRJSNTrL0PgicuKvWXltneacxVHogg5Qw1aabC2Mxz3cXIvwkQBWoLl5KfrgxF3KsMjPDsoX0Wz2T/+wsHgFUPB8RoJvRmW3/////+irmsv/y/+Us6oIjisVzFmZwQNNIjlXxQhBAiAABaO8lgWhJzlXTJiM0dMYAElrCAyjnpjmgi2M8EdvhIEanbyR8IgrIbeQOI4tWrbRscD5aRt1Dkby9K0x2V/++/Xd/8FRsNYlHJNXz9ZxzDFyHRy2vY2v/+631LkeSsd3RpJ8+XLN2VGw/OpCg161FAYe31NJgBAAAAAATLxUOWsUzlUVTTpgRdQldC6Uu2utNQmq3kUWdNuwXGUMPdxAARPZktFrZAIIWNOXG0KHXbR6eNREr6lZIjOrro1P6NhQDWQljMYeS3CHG7gx7sNn67Z8Sav/88YMEQHAwmahXpsdxTjDf/////de1v8jIqf+xiEFKpyOcSFul83QMAAAAAAQoWCA59WIGJo5lyXlP5UGpHC41uOpaGgiLNIUKmED0XaiHIDjD+IWln6WMoOMLsbx8hpCjOLBg58J3HVJXC3lbsytdIE4uYNwPJAhlv/5SWK2it//pqtMYvb/E2dpJCU3HkELn//h9y+uZaUuNzY0PIvLPc+HKdKy5RrBZYKkSbqtRyIKKSXvFAF3iJ1EtByjXgGVbKEAT1h8R6LEQukZYYRDCWINQlKP0NNNgYtoxECGNKguJqq01YZqCpbFRYLlP/+7Rk5IBj0UjYew9aYIcrit9h5bZRFSNTrL1tgjsv6v2El4jJAMKp24yqEwDIZ19GZF7YRMJiQpulGsLDfKeoYFIAAFNekUoR3xw7FCk5vK31VZO6nFZv/////SZlXk/u7zW/5yCjGsLjmCQDEOgOhkckcgAANny7o0lKimXCQHnpLJCK3MOiIqIBLIQgyaQFASD46N3Yg7ZvUwl34XGZfCBmaPCA+HS9c5Xgdo1ve6FYy6AAtAXP3We700R0e8rPjRQcijP///qqDAdiBn8flZqWWZO938JS1RNHVYlUm7Pjr4NTJzDiEmZIIC+yxp0oWWio711h8bvTKt+Q0UBBAAAAAAk7zBwwFN+4+yv7BiCoNAL2ZWw5Q8kEp2hDNj4YUBwhpTdZlEV6FV2AOrBQsJZAHGXoTfWPH6kNQDQu7SQbRUbgNfi1SPRunQmJNX839n4cwLAZ2KK/fFM8VlTXSyp/6hAXYZ/u2v/////+r6UapmopiMRJhEV9P/F8Ei5Q4Coa7oF7YVtiBwy/btIMCQgsC8YuAPIqUscdXMRgqqhwtySQxLJrQ/Gpg329nHCu1SVQ6i9RYihn1uVqSRxiLQ9tm2faux6NqnySqB/2rLgXkR0r/1EIPTmvvn4RhdpjZCyD4v1mJi4fv5lIt1WYod/9isQGR7igXsiyG6JZgIiA+IGDRJxwlrABTdwXIDBfSGm8WFVhYstcvuytdbUVaoFWfNtDXymA4idwom2gMEmxhdkcR7Vg0T0ZGjRjohD/+7Rk5gZkSEZTk1hb5Ilr6t9pZeAO7SNbrL0NweQuK32Hltm4kc+WgbBCIinP5gcFQTM4DzhUZW9fQ2BWk1qff2sJT/6////////bJ7f92/6+cw4joxUFUc/CWCBQAAAAAASXE9QIUgEOUJSwAgJCg+OUItQ1eTfGUSzJcFdiFh/KBXtg8xwE1iREidY7CmJKEoFnOUvEAfckl3zKiSkIaRbuPRRIalYKsZi4l1Xz+Rv/IfZ0u8ibXa6f/5Aejm1v++fU33sr8L8//tbWe2pKR6dmyGbaGNBYrXrsyxXGouEaGffzSKv9T4AAAAAAAAEyshWAuzyWNJvNiboHIehA8LY2oFzAYkZaQGSOeMSfQSqzrWVw5TA0gCAwvOo2EQBY8SObYVJULd1p7f5sMf1pT+XHjTJcF3pZBUrTdS+o4W6LPEbc5ISjwdI5NUIFCMVArbufTj/BvsIwelxe5f2VVQzr//////sZapql6/+jP99HIOlxuy1RwycIznyB+WxMaalQ5h4pfYRhxwsyus5jhoQLCLpY8zkGFITy0HewqtKWhoppa2R1BXxFDqcxgCxso/5ji8bNaKhPEyPBcs7PnFUsQkxKIARn/0pYwdxqt/v+ubF4o9qc6f47OWp6w6GyRKZ/myi71KUcuJpAIwfTgWu7lG+rGNnZqOKsBQQO5j9/rzARJb6CEHJYQmuux9CMMvwk25jlKciw4cQWaAyKCq6FnCxMtVxdLuwlq1iBAIeGRhcBKtCJaLzPs+Ka0H7/+7Rk8oZka0jVey9L4JbL6q9l5+BQdSNZrL0tgj0wKvWWH4gQ5I5E2KUROfl24q3Jt4JgRIuagGKxB/8orQh2VT8RuOmatfM/z2Ml1it6Tv1+md9L//////WjMeqHlX0/1VPy61PHGZHR8qVMBphYYQ40oLhJ1IkAAAAASS6gh+RBQXY+IONIDitnBERPNgSITOU3xHx/I8vo63NqEqpdqhxkUIKIZCEk+ivy4SqybOfAOtSFKSZOLEZv34gULgmIn78pNUTxqOEUf59TII5XLqmq4tttrYcuapP90X2/3mrkLHU8oJRlKxxq60zVNqYSeAw2oZ/RhudECMAAAAADcfEZwHNMIwlsOXPFZkzGRIOvKnq3NgCaCjiYCtyLDpQ04+FPL1rRuGwQRGyS5P3AjLbF8Ej6hoY3eIJlHsiYOxYZXCI8oqHA6Hi9tGuJByxanZ8zM+95Hej+9L/k29rZjt/////+q5WNn0f/f/+U+vKcG4txGcG+aEZAASTxc4HxayFxWxpCAUKMLKltmIsphgOLTj/F0UQnSuS8oCGaRwpXUjsqwGklhPBzp8mJ/oa83q8NWhCBBEeOk0oqshyx8GwrUq4N6i/xvpYwK3y///mKUYlQ91Sc7fNWUZJ3joKQxT/1//nnhbESa5ONhGZXDZMSs7cIbdqk9sOW3PrGJqLO3YCeSAjTT4xukgIxjwYYsIBxsBLtw4km/CgSYxfwNElaI6sxQJUAgBExGRcTlShGwKqHqgpAPZeUOO4Zgcr/+7Rk5QJkEkdV6w9bYH9r+u9hgrgRlS9XrD0twjAwKv2HnqBYS6qrem5AKbsulsuQpLyEHdeIuhZB3qc60IbT2LErlh6wOdt+n46hgoMnKo6h/pav/////6vqc2rzh5XXuqovS1DJ5U+dW8bsErkUc6RGhSppY4UwAAAAErmlJaMtqPCayJaVuBPTaQt6q9uaVS1AsFi8WtT8FZcZq8kZEZy8tl8qVAwrvqm322PS0Wgaq07jV7xjzKYPl//ihdv/8aUSYPzkzDDebFRYXHisiCUPHmR+v74xXPjtosgXJs4ZLTTw8yEg60UYeXWap/dPTqAAAAAA14YY7EnTkCHOSmYgo1W52FMH4haUifIgCwtYRKVlLlNPl65xAB/2VpmtIYc/iDywcB0A9AqEp/x3TiusM6HTRBLyEgOAtRwwKpMFYi3HhLCUaiwsM/6FGW9V///////+r7D93ve9f/+htkZkLMtFIC4YG1GHyoTWQgAAAAensCjpSlKJDiIAaUBmw0m2rBHeBgA4cFiiIdxWWSxM6A2xBVUFDoYoBXLbDGZCBBEJrXx4ZHyFbmWLX8cdvSSGr6YfKZQ6+FE0Fm5eJIjuAIDaZmZlMciMtUNux44unj6QeL/PblMURO76npiL1+7f362zTl8SSJhTmykIitblV4SOoUO1JLtba18s9bysSzSgZkAACqXMJhAFNcgk0GSw2a0mt69S/YjGXTL2snT4YEydNkWCg4+o6JVVJAwrU3HtpVvYFAkZ1BE2mkv/+7Rk5YIj2UlX+wxEsH4L6t1hh7RSmTdPrLDaQkSwKv2Dp6ChIlfLCsK5nS0UMytv8ZLKG7vAjq28ddiL0krR7hcpd6uPExECMOBp5JmflDoweROMyy+Z+n/////uqHHM79XbR3bp/+s3+pre9gkqPFFTCb2Y09l6cYMQAAAAFjoFTTdFFUTAiTMA0TIAQmZAZQbPs6f4anR0aTwQtPUeSk6QhwRS1IplSZTG2EkVGOT382OkgAqHYeUJaSnK58gz5Wt//EI3x38pl+TyuE1Pf26TY9dXa1OtFev/l/L3qSo+jdFJqtvJzL973J24fVSQePfxU9QstNoDIAAAABxMTQU4gNi2S80PzhIVIXZjzdEFA3o6Es6DYDZS0MjZzRlvXeL/AJMPBQqixvKCSApQsRGVm8EEtDIDMYJpDRjvkU9swHbMWAuyPfkyV0x4kNOJhUyqRaHnKIHRfcsyCUG4q8FkB/O0b//+lygk72/stgnKgYOMBFQAAAACGBowIBgeUJHBE0dFmpoP+jOuBphVMEpQkTDVAABnzRXJaNDA1gRjEjyxa9ikeASk1VOFEIQAfLKnp6fvyh+wcpCSXrGiu3DDSoCjPMbdMrCoYvCK///BAEsfh3kMQcsQSt5ONx8pup7bpVQ4uuhCDSuU6uv/ln0eUpKThwnLLPKiK8YVqGsS4zISylho79SuPPnJAIgIABGPT+Fi2QFr6FJAUFNWdAMHCtyTfBhblkKa3VvOMiEnUgNfQWHcQKHhg7cXTEL/+7Rk5AIkAU3X+y9bQH4lSr1h6bQSzTdNbWFtwjqu6r2XntkwXFUcbgl4Fwi/afSGj0kQyK9uW46FjgLJXwifsr4rmBtOUcA3TfGGPFinenXHVrw+mJWVgWgSYoNChAbEzzOZ9P//////MQwc7nff0zP/nvGnOOog9B8GC5uW6tQMgAAAAFDApSehy4QLjhWFZp8yHsYApvKhkb/iIgcg4zTYI6V4sahQqVBYfh+EjaC+ogkzhiSA8/hWJ4XErWSDhiZJ+wUaUTEhv//9bs2f1zDjhzHkGrs27+QKMHwVRAo0zsrvf8eP/1lej61dn0b8asgoAqIgSFx+7XrZ458XkcgAAAAIN9+0rn3mazxtIC1mNHeClD/M4fIZS8IOKnTDMOK1uTgrMp0lvDfV3pSg4dPBDJUwnmnHvUnM6tSmrEXcfmRYdiLnwKbEYYJiHB0TrmnNMtJ4tJ979viYcQMEQ03P1///////ajs4pfybfL9PnH39thjCwqD2QeowIq6DjDoJgiEaUG0qz3rnOLmAgMkcWRHg4VID2BYjNmAVWSPWDFJXgtbP4eqqXCFAgMgGQmpMIzLgtNlYtD/P1EmkDuYjBdycksC26fcqgO+vdpjj9//+KZhMPhwgz2vPTj20KS39md/qMEDYoVbZ1Hfq/Cp/NY9zYiscKiscjrUiQ2/5UWEeGUgqgqf/Z9XHo+SaAAiIKiiptgjQ5azJw0ehzMkFAKCaQBIC7CdAUhCpJosAYJIceMElncBgLDJGRCL/+7Rk4AZj+09Waw8zYH0L6t1hJdISfTlPbWEtyimvqr2Vi4lMrTcoEBF1UJgYUkwXIhydj5CJAVa5FpJKVzztFG8rS72ny+Jylp8vlS1nVbvytI+FoxJ6u9Tls2xrA9wv/Mfz03//////SZJBTU0OzGWarP/5325950KSiiE9lQ0AAAAPZ4QqrwhEW2XpVwdQJa0QkIzzQqMzpnQYqsd5lWilhsJyUJnH+9bdivmIWhf0eN0vDt4zzf9vFMPM4myjm8h2vq5zKSZjef9vYQw4HSL/NVJ5YUSXipj70KqWkwgmh/F/Kcj7QwYYkZgKmKF0FEGx1E0ND/o8zI6xjsIkOYEIAAAAAG1OQDFBUb52HRphDhIQUCuBpCZbFSQqplSKYqhUrWe96jNGUObOxFhg1FHogQt49ZTlczTMgalhhxLR15fcVvLInyq0ha+W9RKyzo6pXcVTAIkBKUcUjbcsQBYJUh1bqh5ExTW/////+lTjlOyLn76sOt1+1Lanvsej2NNsqE1rkIAwwhOItQgibAp9/AHsyqRvhDqZLKmfiRs6py2D2cIAEs3h0rk/E62izlcPAFAHODTPtmXnf/65H25NLi+et0eIzdac06rHKNrXC5ahRqh61KGogATOsn9fktwXU//+FSDs4BhRAAENw4e0oeq5nigqEqlohwMhAAB5zrJBZXVbK+w6W6IGvArG1twJUxtRVawNIxmH0XYfftZsrfh+Fct1Uxjpbh91svnMMSZFQdSiYbtJWCL6B4D/+7Rk4IYkBUrWYy9D4obL6u9h56YOpR9XjLxvgfCwK/2EiuBAZYLwCSKMBChbkfebhN1J7txl4PGGYQh6ye/7eFGUCL//////VtnX0fRv/6foQqITBEIc6hREGoZgEAAAAAAIl0AjDHlGGAQSW0MoLhsXGFkHcWPfa+wMKjxeP1AwEPXUAGKzjyUSBPEdQ3UymwJAhguBYzmVOP/1OFpFYa6rbVKj/rO3qOfJNatre6p4a5dW9nk4CNWUNt4pxnLcIfLm6PZTxn/aWnd9Zjg1BadO88BgO9fH+sfYyiwnLWk1lf64hgAAAAAAAFN5Ww+QMgRARA9xIbNOHLL3JmvQYBMILuDQ3tCFOOng1xrTOmQI+BUCcqeqOAqVcIyiAGRgwbXqs4yRxI6+UlhLS3pk9n4aeVv2t6sr1baTySMxiGKd+UAIEwYKNNMIZm+poOQ5HOW1LfnNVDv/////8xDXMNZX/pMMpP/+YZMJsOl1QH4KiMKxsSQObZpBTMxAE3fVHx3+EaZAqTHNYFryoKuMvU/BWEPTDhrIEiEYB6AurYEo+JzN7pC0IZXhJKpJZd/CjQHAROYsXT/RDXbKm/KeXyPv9Bki7lnk3cTzRz2cmMFomi//4Y30ieHB0eeI4vZx5z/eTMzQdjpDt+GkX/llQAACHAQQVZo9tOoulkdp6ZxT7maKYoB3lGkCZaRujjE5FWMMmdUjsqinCXyMmsBGoaoAjUBQ1MUMFAGSYNHkQSahikhG+ACw2SIUAhm0/KX/+7Rk8gJkREhVe08zcJRLyr9hB+JO2SFd7LEOwkGX6bGsvPhjAYgjAQYEsOtXI9iRigG+dRFohpJ+W8L8XEny/olSr//+fA04JrWN6hxfjcuv//+xZ7ukToK636JmHAqkIBAzPAAgAAAAAACD2NhwIQA0QV2hQIBgpzlyA5CQpavAGlkIQuTbRAO8IYYWZ5ngUByCkvTdWBwGoBuIQfoFQUosJ4oVr+RUl5Q8ALhl5jL0+/8WVZvkGUu7Zt5TIWIFmiHXa2LjBg8QHtNY+i4NGPwTkHf/jNe6RCyyhOItG26WJQxqatDTTOzz7ff/ysSwEYAAAAAFnODYELx0JnS+kj2Sm+Ihmn00gGAmSW4TZFawoe1kFEK0qWMJ1CxmYdSJJwMwPsCICpZzBP5C4CuEgLGddWyChJxtUXCMfvi2t7w3DfJOxrDIpViM4L+GBifP22n//ri7Nda3//b//t//////9i1ZvOrl6fZ0S/qbAgFMgAYOEFsFKBC7WGCAAWXywCg2mMOiARhHekONtRdDusZ/JIigMBivosvJeVop2odoeXDcFUwjIRZkjfhHvGZ2DX+Jl2Enb3xYW+CyQ4E+AgAGDAhR/+wdh0WIsdMkGi9qabz/f42Q8NOka3Ztf1teOu0G1kFQhgqo0VDk4z+YkOz+mardpP+xvZ/BCIMBAQAASE6qyPSzkoZ5BWudkt3UQR3WCVKs8LGTESiLPC7hoKXDiuYnOhW4Ka8+kc2wyh3ogqx545AE+VhYla6V1nn/+7Rk7gIkWUdUe09D4Itr6s9l4o4QQS9XrL0NghMvqz2HltkVsW4S6L+LsgFGkDnQxHaO9mQ1UncbjOpnCC7YY2f9/hKVYlJ/nX//////7oKVaWggqfo1ycuq/e1EELC4gRJARZW0gkAgAADaCUyAk0BC0WvLhJunRUzlCU1F+GeIhIrhzbHWuP8/kYroPIvlY0veOH3oaooKnul40h5Jm64OH//wGgq2qfc7As9XjFEOQoLzB0cBD8VgHAaIrbu6Dg0H2HDJT9TDx4y8sT2/s5GnP2fE6JxhAKZiQB0DNLN+mlb9zqexcC1Tl//qvABAAAAAAJyegdGg8DhHJg9fB7iCIZkaKTR0BqtoAIRRBWShSoEv4dWol6IASRAu9TgIp5lMkU1VQEa26Va54wmouiJMjgerZYW5LXpO9dDKmevrKr9tY7/TzCYk3NmjR3nk0Sh+hsUsTz+v/2Row4Laf+jK3//////OjF1+Nb+/++XVXPFfCh8sRGwZtfTTc+duDQAAGIdEDS9hMM/Y0gn4b/qTyqqIS7gsYnXFC18osr7i0txTFLmOhi4cPUy43dSIQuR3MMBf+DOqT//OMCgSW7DnZi2UG4SI/kEH4fxmoOP/zUdhFTrnuFzmS7Qfq+z+kqe303xZpX//MO/r4fCapT1gS4nW/XYk/cKph89k/R+mFMAEgAASj4VGWodJrMPvE8RPVKJnaklZQKUmAgGqInq5SOYC58ML6iaZjXaVw48MkboZBqBLeZZFvC0sDAv/+7Rk7QIkQEpU4ydOsJJMCp1kq/YQMSFTTKzawggua32GCtjwU0qks9V1bCwSx2OrlwSl60e3aypSOB+0dQX2Cc+ZdgABQBO55ztShW//////1mOuRBqSfdv9H7K5mHskMHAWAGgkTZQAIAAAAAAAAwzuI5sJcQ6BLmrSjpjKysKKpQEXepNUwYAcNEWgcR1qeVo/NDib7uW3ZkNwMEphqpUYgCu8wuZDd68h6AJ4WTId2IiGP0d8p8506W9XtH//KDoATMvFBtrZMGli7jb3/HtZF+o7hp//0kpB1k40VKEiFOWPcltjHkfInHuKoutFupenuqgyAQIAAAAAkXgRKBzX5icvcuMgONUvV/IMIOKUoXwsAkCgDMkUWWToYDDLuu+qRBYInMAovQBDB4Vqrd20YMsE099V05S6inolRU2e5Ez9aRJsVg/WqjkzMLrpYJi9uqVI/2TPp7ny+r98aiU/0w7cV//////6soymOV5ymbqVqEt/mUjFqRVEHO7nwRxmpSBwCU5pWAPG7TxEEpEooMIERmxyFPu/6aGidgKcTQcQjxd3LItNA6GdhRS4AmxBwToxGQvR0sOfLvw1chI4SdzRmdy0yVhhSRcO9b/9rBLr+2J0aNVWxPf/8tHuubY2HpQ7//nYeOIlZqSjpOsl0+Jbu7TUD+YSbeetStbrOfZysKICAgAAQB0JQPI6c3MalYPpACq8OsueKKyxVqWQgWIArAOpmhFH2JPytVjDloLJ2LpUIcunaWYCyEr/+7Rk7AYkbErUe09FoI6L+r9lgtQQLS1X7b1rwcYrK72GCtjJEbEDhVRxO4JLJizIcJ1FD0XUicpHDChqKb09k4wtihhVyu6df///////////ruDONXvGm1A0dYZAAAAADEpaIoTDActCBFyXbPTMyFsAYmlykSqZH0wBZBG77JHTQOnPW+mAlbBDiUsyKhxjm4CAAkJSKis8NeVez5TxAkkFU0KVSJ3nHmIX+aE4JOn///hbic6Xjpwiak7ob//3SBQBtOeQNBRmlJ5vZGgs3vVXMog+aq62d8q2mBSAsEYpt5p7er4gVAAAAAAAApqhpelypI4SjCZp2W66yAeRA4gWtR2DHZZAw5dQMEljLB2Aq7GsDLyJiYAUBiNI0sUTk0gKGgULSTWmotA6uUqksFgqOVKYM4Xo1yrAzZWTNfScdCTgYUsDEX7Zgnm7zkwOXNCMJAfCk4EiBe/lrMr3CofzW1Wo96Zh4vv/////9WZT0a9+Z9On6zmIkFaex+aXl1AQZqPvsxQAQJJeKJWAUpFZPcJKfYyNdQtrRvHKE2lNIBilWpYk12UWXnppNvT+tXpXwty2kY4FY9iBIOiYYh3UVc5BQYw9v6Fo3y+alpC/3XzcbKsOYnmqVV+/668IqU6LSuNnyEVKCMhS2KW2+KmSaVKhU3BlHX9D5AAEw+0Rz7kLnaeLHAy4FOnXUUWKF1wW2YeW1mG3iXs+yKcna6+yYcBBgBE2MLybEuakcXimUQxIFjkpqanz8LTK8OX/+7Rk8oJkaErU6081MJ7r+n1ph+IOrRtfrBU2weMvq7WGFtlK4iGhnAPY/7EwdICVYhRT/2mZlTxcaKGpsdGZypf//////po////z2MQyRhWyvYPgdnsKRqiAAAAAAlwyLIlylwFXjQwsBzsxigW7K/FeqhAh0xRIaYKBfXrbRm66k6Xwl0C0r8mBgttNNCWhIRdcl/KePTsl1pmy6x483SPrb/W8rGldvtAa8bPP//PFLDkdvdNDlCYVsZlIMGPCPlstwScMH8P6k246EddVGiUKiAMZ7tplbiVAK5vjAs1XUc9La/kAwAAAAEZO04ZDgVg0AxyMHXKzlNpOxMsmDUMLtpWGMAi8rPBLvxBHbAhGgoeSCAmRGY6LBOgk9VZM2Gie1djO3Ils8tGMQfE79fBqsSYdSU8PVorML4YvA+4Zs0sM16XC/KL9bf/8CEBw4YW6vmOdlv/////9TCRBNBpSihdKP+pfm8vZSn7kJGPSPVJCFEWbUOD9k1RBBDpUmqDXS8aOqX6+zsJVGi4zJ0lFV12BYkrA57V1HYvCrqlzvSemyuM/JBiLUIM8wgxRatbkPNdzNhAQkZqC3IcemPe99VOlXFmWBz///7BHwpP6Yr2KOMMgjbYVO3oH9wYB2hOE/50vxkK8qfVHBxIAgCG6aQzseXuYzLZz93T/rtoIAS+BEvL2AwQpg1wzLHeUzcUdDUuTzLzqRpIaWJKlcyNBVmqqMMpntDATTIQMuFhW6ISGMuYqlglY6iDWht7/+7Rk84ZkaEhUY1hDcJYsCr1kqfYQdSFTjTzVAgUwKzWXltiFr7hthyuE+yqEgBQj9gMwQZ4lmBsdsROk6+WKu4WIGfvY72jat7//////+/Ymnr/o/7cXKbEBhU8TDBg4ouhBB7DAAABS0nAcQpoGCAKdaGTxHGgy/1MUwC8wVCzBQFVoKHEO6lD+tapqqanVP8/cnKoUS9EgpwHyIUk1Q9fq5T6MwlAhAvypS8FjV7mk1rsb46zCOBZ3//8Hp5Jd+PivYeCOQRkuez7Jp5510knaRPL1vOsp38d+2miSSx5RFSHrTRSU2FkcdzX/0kn2f2ukAAAAAAEBVBt/F7oIrTzkogwMNX46FUuIApbpCkhDhwNVABO2JBYC2NgwkTTkLukAcv0th0i8gCkA6l5GynGAUoPQto3S4HSwo5Uxm9WMTAPhMh0n0nh/t64Lq/AKFZpTNJ5sigTD2IqIs97fqziqhnq3I///////porOrPyf6q32693KzmKzDBIKMUTjal0BhQBAJH+FzAdQ5A0akQgEUaH3BKgOVdHIlTMaIyDR0omKxHj8Ieb09/1S5iSs8Uv0e86U3Egx3yvPSOh9rPYV8f8mJMIEv/38Vv3vX/5GgsogPjsyf1yEfD6xE2lFx+3t77pvNnaZJA4QB7RFFcNLtIQcXdmpHPiJeWh0BzunbCMBCIAAAF8xFRgF0Y8LBNNa2SWKjeWMJgkoRgqqVwtRwumXBQqYI7qQkjYG4biXk+xAgzNS1OkWAoHxhqH/+7Rk7YIkbUrUS281QI8ryq1p5ahQHStd7LzNggivqz2WFxEuczxrLePRaB6F894cgahCLYisdhmdkkSAGsTyAJATHr1Veq8tMzjZf/T//////+rEOe3///qx1SSczJIxB4xQ4UaNB1bUBoAAAABEPiJMFj62iYSnYnzFjul0twaRc50lDS+owTgSQq8fNsNT5Qkm8ve1rgjDlvHaetMlbq9o/IGLyulrQ6+qT7ytvC7ElpMbPt6QqwKL5/0HPiV+kk04+5PLGA8iGVm1KhsM6kYGL0x1z//9wsCjTKWOGHiSBZ6fppSmD8FofFCFm3T9Gv4gAAAAAAFPF4zODFg1aMXVIAZjKsvVylGmPUbKvcMHrHDESvCQEghcQvekahQpNchchSswpIyw1IuJMmXKmAdRbVMGEYY1UnAJibqnjIgqj/FhQ83Hov0G2pU4x0l6foYuFo/jPRkSM+vn/+kXGlM302yPT/////yYkccRMn9myMT9VVg4JURWuHjAAgULuDGYcKOSASpyHkWy5wMBS+T7WyeRiPixFhbQi5LQAamYajhsTQ1LJfRL2pO2B9nkjz/M5EjovCVU8Wsd2A4RE1Jkg3Tvk8aGpqpH8p7CfLt0smYXvPGpmcZz/E8KHOaU4t31/bmQ+qmUqmUUjegZDKCswGnB7ooezAicF7ko0tZXBMuTCDLAoEKiVUfRdinKRS325qqtgoZyG1dOkg212u2CB0JcbUZl8If5vTwX3LLCnOLEpFEa2TEuHdSQtOL/+7Rk64ZkSkdVa0lGoJNL6q1p5bZOWQFbzL1rgdywK/2GHtCENAMljo3GBMAoTqe/8dlig3dP2U09rU//////6u9F/U35vvpl9GTrQakkQmclBPXNgkAAAABJOjpNhjrpKllxkEqgdN6JEULnOkaHVYgENgIZJT8PRWqmEE+N8fiQTjwohaAAp6NYozBCHtagV6zBc4hwCySmC/Ym58u7eVDWM+X+Xev00VlztmT1/XeCTIEkAXBipylKUcrxRtJXBD4NeXu6hUJQbpCKIIkmxQmbQi6RV04OqTOous0K1Hs/+hwAAAAAAAAKouIVLpTuwakF0B4uL+Awejw2EGIEzzFMEuzBhAVHEaMqhkRlWjUmGDPghwkW1MYEfURyzbBi95fAGgFKxIuuZZ73JyLVfnFkShksguCKeOkAMSJBgBpjusbQHuMyhPVOdOZ53nWhXdlsqzovbjV+73/+PjweKRcRN/vHVN//////z1u0bMantU7nK/T7f7jfrpunkqfoki+HbTclNBEo+EO6XTdmIryCCG9MaBliQzNcHAT8RDULaZK3/oue7jCVjxmxO9ZEz+Ke6swr6iBKPo5A+DIJocPhS6fUoXD6DfxtZKVbe20HIaOERyr//4oy0k/c9BRTG1pErp/rHEzWswU6a3b0W2klE6PADE2gU/pB7NgBhzlQBKvToQ+6KshwpLtpXoVUlrPTCMlavhYGQp5Nna+JBsgU4faHbbxPwYoChDc1tt1YZi+TWp1MGtN5jyXNYfz/+7Rk9gZkekhVa09LcKOsCn1o6fYOtSFdrKDXQfIwK3WVlxCBQABe4xYO8reB5loiw1EIdjrMf7/iIUHQgQPv/0//////6nQ71FUZtTr+1v1bLZhrklLdh1EsZQz8AAAAV9YoYQzhFsgMQmqpGb+oKLAhw0oiREcosNXsEblGW0gegcNj6jkJrx96Upi2Ku1FFNo4zS74eFWqzsm48iEztr4/3sfeoATE0RASn/+gzyRjJeO936U7VYRMje///+f6kukpJ+TrN25JQ2ReMWapThV5MuXU8Lk2ietOzSxhsxnzwRNs0Ns/qsIAAAAAAKj6ww1M7DEadiNQ/IzKELCCK5fUGAgwcwwDAFCqYNHTyIj0cIDCwDXQw5fRelXTiGkYApiOACAZDkHTC4XolQj71SiuJJcpB1UmCnTQvIh7jjVyPZx8Cv9fYYOilOuDEhNz3UT/4oQHpRH/6f/////6KxRmj42Vq2Y7+r9uYfQXM48cK1NHwyHuDwtRiBEXH1oAJFdK8SKUyP6dbLpgViI/unbchNsQAQwIPB1ur1bkniGPMuYjqbK1nPEA/HCXIqwcrSrVOxtvhUTOxXUsXnV3rlEiORSIDU0jF75wYcwWnu+/svBoshUXbyFZ/01YSdcHKjr4+W+/Ww6ba7S0NXNNokFLulXg3q84+jbRCV//sYlYjeEAARa44GHDuoyh/3Ha+C4kaUbGHqGrqTCMcBJkLgucoQqk1t/E+WSBwKLzA3iLAoXQLolrUUndaQ09m6L/+7Rk8YZkXkvVSy9NkJYsCq1l56gQfR9XrT0vQh4uqz2WH0g7Qlmu6391zYm70dvazh1qsLQ0MdyI0YBOXFh8QXPJbCZo4ps703HEHArGw2c/Tfqn/////9T26GW5///57UGrO6shiguc0dGWQhVJUCAAAAAACbmaShADgFsJGl5YDMatNYRAOc5b/qtSWW87Lo3J+fqrUc5Rrkh+kWzOP5NrMt0ZBP/pHWBWIh0p5PSaX0sjB9ASWn/xjgmMKPX4/izRxkzVEV/pK4yGEg17v35i4keQ4ssGA7THhgg0m57iizz5sTCaauKOD5jV++xq6meQAAAAAAANJ+dW9gikAQFFFHScBgyc0VRVTEIQlbBYAOATEVw2iXERQJuCkmyhaS/US1ljSiHFJJkcGt2cuWN5GYZuw/X2+1Sz9WUr5lwuWkQfni+JZoU1SWpLEmJc407b5zueejPfswuv2xdXuxv/////+qs1CqfrP2+/9bSKdYuHhQTD46KARdQZbhQkVRE0oGXsTkNIZCcQinPcChTDJeSGo6DVBCImEgdFFenp2o60CI6wQeoi7p65hJJVsr7X/kQpzQ065VmkP3ZpIDxrTpB1U8mm/hOUyJiGtjW9UJQQJmEavW38wUr+fcbV7a8rx4qSjpngySGpuo42uxBL65CcytV/+n/6P2nMAROOehU8g+JEXYEL0D7l2l6rsQBtREZV6sELuxVOhlqncCsQhhAYyxEtXrgQOzRXTTn6fZ1T4RbEYTzkuVbMjiH/+7Rk6IZkGErW+ylFoIvrmt9lhdRP+S1XrLzPggav672GFtjIFoIgwXqSqSyuSAVf+1090BSdrY7TM9MxEWGgccZFYT92uv/////9VtvWxpUo/3/8zFIWjq8aKkAYGINUTHHVVQSAAAAAJKjOkR1ZgQQl8SCqCnxiNKJDI1qoJCgAEwGEuFfNfdnUyP1UG8DSVS3K2i4D/QkkSaOQ/If/7e9Ms/ySlK2ZU0s0XGF0wECOo08wpuNoZNGi0QPuXSxcdILSM8Umlv4RvaRms9V/tdc2IYyZDIBFEA+zWchMYKtBw1Sjw8NIFDl1/yRoAAAAAAAhEjCWKy1iPy6gwQOESIgTbQKqUw4IKhTMjSoQXWBnLTgYiWfSsQ6s5HrzMRLjioRmgmJKLPDpZkDDwbjIT35STVWf1y2FMljDK3cf2R7isBKHuHlHIAdprsPqwQHE4ht3Habm52GpTDNJe/n/UGCYoP8f+///////RUdWeXuQd09v384vZKM1HNCIqzY3ZBgMAJqcsFhi5fdAM/KNVg+xFby/rKog6MrCgwIhBphUq103pwe5LNWgn8kCFmMahNm8Uvya/UqljkFLqS+dthMFu0ugQBTn+d+/YEJE688r2QEhFTd693/9YvlG4TXK8///qXwonG4fJEAOKUMtsZnxAxTOyCpl2LNUnlTB9t/A8GQCADXRGA+J1424PWkcb3voIgNPXys9xwS1YRJBWMME76harG5OYlkoKy1WJYiGb5mBCgKijvz95cjtuqr/+7Rk7gRkR0dVay9D4JPruo1rJX5QNTtZrLzNggswKz2Ei4DuBZTIHJicS3Eo+0t33niGa+qSOOE7SpIFqVwKUCgpUascvPv/ECBv+v//////9bo2+ZGN1f/v3YWOcjI5zsaBgRZAQmMquglAQAIAUUybo1GDQ15Iqhy0JF8QEA6C7lHWDrMLoArCneB8B8rFEUgla8VD9KEqLyJOuC+n+dmNUiX7ejh3LkbkO88v/8qofnCXKf//xC0P+1rFFDk4LoztA6P50y1Fgd6H1/XqNehmUjuYIY0cLiAKiqGPRZVQYZYqOFLhmQKTUzZQfT+BolAEQAAAAAEudCQGJbAAjtEhx5QRIWki4ppJY2EDCo27J0wGBQlQixFOGct1XglesOsBPiIBVeu+H13zjJYR2JtRJhhc3EuynKXUsdxMNmiq6xqHUylCXmFNdGxSWHReaBFg78X+g4LRFL/+e///////nOrl3bpFZNew3Y0503+0iRMdEPPPVIXDjMTif1BAAAAACKcLQjyUGgVV0KwESYkBwZelRx0ngdUxhFRoiMTVx4/nMnCZKut9LeLpwW5g8GU2YYwdNitBeGN3K++jkNnU7hqUS+c/9AOBeWA0S/yjCMKhZ+co8LhuEhU4cPRcqPS3RyZiJ36vhOddx8SkK2wQJlGXe5drWkTRpfhATA0qeEj/WibUAFpTg0gb2GthAAmWPFPuKtqoKbt+yWABGIMptyWwp5BhEtSuIKrjACwr8O0yUOGTeFTVqMMYzTX/+7Rk6wBkOk3Way9DcI0rqs9h57ZQ/SFXrR06wi+wKz2XltgWCPPQdY9xm0X1w0pZ5SId5nvHDuJwJ6QdkNxWHy6VSBfTMb9Xbp779BYPqJf9FJ//////zo4ukYLXagsjl0UgrZfbjAwVQaRVEjCR6uJtHxCL1XhAcAAAAEAWOdlwKK1VB1VVcsBg+BmIxt3YCvpLJHsEeK93drAjMVo5YvCAV1yglG+RwR7ZcnDlcXOfcr/RyMHHCon//9Vf/9hoOBAMgoaSa5460D+zquEmlofX0/zcTBr2ocsURI2F32UfegzErguZRh9bvWNiYJAAAAAAC4ZxGV80IDCBAI09uZV0hkIE8UDQUQIo+pXshcRdk8SyvXcoziYEtSJCQEgXEgYNguDRCb2dnR0Y8av2t/F3JK/VF1XOo0MYbCdODHnFDymZfiG4T1xr/Lg+B2Rt1xxnGr0/////b/uzbnKk37bP9uhqXRTtDTCwjCIQY3FUA0AAAIPZ6HCC7SmqYcTQoOynQtTVSSYCYgsYgeiaGJVjVoFv5VGEGJAtZ7TYSFENmKiyDIkFl0s0ei4Rn2+GQCZAkGExIi7YHUNR+YhhYy5GYrs//9NgeITaF/krcmSVzoope14eXkgfk5fc1S//vuth2LyO2jYKrChaZCNsbSs2x4dcwMsaqMp8sqRAIAAAA1I0WLYKnJFH3QaMK1cqqCjbJTBlKpRljmagZCZNaDwlDCaVIYQBgY1cK0Vyo9Bg4BwUESYMkIcNa+/R1gj/+7Rk5IRDskZX+wxD0IQLqu9h535RgRFRrT02glcuqjWXltmA2CSDnERVzMGalQumaAnjPISigg0NDQWo420ScxlYWETgt5lKJKLzK8bHD3vrZ1DgicYH1optXEG1////+iNr3uvXo/q3J3+VPU2RSixQONQoKpEGAAAAAAS+MAKoqKVV0NpOG5EoChKfKKL7LxjgbSW2XlVgrIaBBnKO/MBrCWmyOo5SVKZC4rXHi/5chlFEeSyyQa5gW1HdFiVB3zf//iiBRmnkJqHXJf/ipBZUqtoT//4uqGUwruWSAxi5R5sHDPdSo4NxRhWh//JwogIgAAAAADD4XmA+X2wvd7+CFCLEBo2JpJ8KauU7zTy5bjriVpagj+562Ern3a2mMrsvSOAUkmA7cgLcO8bBc2ijfARByJtXx6NJqn7HbSdJo2IZaHlNEXSGH0W+LO1tMPX9c9CoNLNo/4jk/////b/sa15DjhR/bRf+vkpiwaOUBQ8t6qKPMVABQqLAEAmGAiphEqfXcePIVJELCOa0A4xDQLAmOCpBazE4Ad2Ay2Y8w+rcH8ZlC12uU4kOl7VBl2siGMsb+AHEFURtNHMz/H3bME1QSaNaL6///YTJZVRP5/mmz0jyS3//8sx8JW+dMOn/fut627KmnXJoP0YRNVEkXmtCVRZshNuQeUWXqkgsIHf/o+wAIKoo06BQtXyhouaOGQ4Qhi6uCzrXF/FUUmMuD4EEkQFiz3MAyEKlHVhGHvsLCRBI4BlUzwUddjL/+7Rk5IZjy0tV6y8b4IcMCs9h5bYRzS1RrL02whswKrWGFxD11KXNDa/KKaAZQNAVklcmRjWTwaF1MZBKH4sDosPCdhTC8D5b9ZZ/PmZ1BAaUBq6DkqhFen/////+9lRh3UkVN7d//031KdiFad1xdZ8KAAAAAAi+Dg6bKaQWIEogKEngMtGTOJAi3IWSglQEo8OHhQMw595JFoLQSJuw9MV7luGB4S19bCRTKWDsaRYt/yMQkIsh1GS63lnn/yk0k/T3///y5oZIz29bX0iU8xN///vi+qZpE+OXeOyX3z80pNOrEpoA5A9kwUfWNUajzVkBv/+MixRL/9azACAAAAAAAuclQNMOQCCSeAhU+57I54QNfwAqFRuKYrS8D3DguIKFMwGGCj1+I3hWgdZQAUAnuCaoltzWCUXlCyKIUJPKxUk7BJKVAroa8oUJFeDpHqYFkax3n6Rsx0Uj2UjR+GYXBdx6PYv//GhNxoPmMZHLNRrId//////PtNo//q+e6L/0coexY/YdAui0JTREi9LcCIpQFuTTIXcZdB+0gEtu5g5owstZW3youIulC7E28SCpQvKFiZK2SnYCYC5qZPK83F0Ua9r4YFYnLBgRBFv8QifbRrpitFn//8EeF1b9w+E8ScfZ5SP86/t/n/22GNOW71n/rJTWiwjVbomZbKSnAmtyqkNynJRbfCj5SdgBBAXjJwQtTTGjqLAxa70HAISUAk6Z9DNkrKyqOY4AgsFF11/tBfJeT4qNLPcJ8EP/+7Rk54ZkV0tU6081sJVsCp9h58QPqR9X7L0vAg0wK32nntB1MgwsnxRN/KZMdaAQtzlWlGu1KvIZ81Tg32V8xt6EOEYqX0zVKNgXA+FDHoS/PHhSGRxCZpeOto//////////2R6mms/8wyh1THzB8Oo2UjhdlIAAAAALQw8OhWEFCLbElMxHwRMsbYjDlssPphj2SYDbnOYIPyVPgsznN6LQwhPELesIPhDSlXwPEPeGJVrQ7w2yBqGJfC4mXkmCjgLAh3/+eKVzxw7fvRLE1ScaSfO2+rvlnHxVa8LT//fkpI4tLXjoByRDVdZNJsuRP1Oo0/BM+vUAAAAAAFpeklk9EQpmlB60ODfusHWSQAmBWgsEEgVCIhBQQGnBDdJamwKwT5PQEgX5/AQCDjwJcnWAcoNYWRGrpmShfzjVNY86IM0uqsVCdUK4L6LQZeXsZiTkU3YbVRqn9/+YqAZmVER3//////////9H//nb/mndBohI3AAhVHVpCnACTCwOVuoYrGEB2eFv2WgwAOBi7wRaqP4xVZysscRFWERhYFK+TMNJqto1UuWVQrJw6g12zOFslJTCAgDIJdGn875/Esn52qU6R7opp//5rQLLGxBX5SqOqSIJT7mw555X5nPv1DYdqqh03Srr9q6aPUuKbSJp2NBRF+w+j8KGaSA39XfFMr16fjPy8ZAB0fg4u29UHQjNfQvQCFWQra4Cp3mCvAF0HEepCIsqGKXIPOT2BtFnDQ2YJvAyBfYzBLRlroD/+7Rk5QZkEkfVYy9b0Hzrqrph4owSaTdPTT12giavqrWHnxGY0uB5liRyst2bcVIhrsjgoYBIC0K02WcXM5yEDsVyAo3w0MPhQKJqZpmt3m2fkdNHgXFRW5x1y3/q/////+jz6VL2+7/N/+KZP/cqNnPGMqQwvwjAAAABle6MhNxlgXQRSQ/mTDBOiPwG+RnJ0MYplNEUTGcUBTtqXjXq4nKgYrtVH0oltDs//atJgzIqv3fCx5wfiUgj//gerL8Q7iCaxuaawo0vX6Co/ZFDqxU5H7/aUTuT6Qe2PmRqnjGEGz6YwCxwqc9fRY8bc4tuRpSawAEAAAAAAgLxtvoUwJUrVZgSOnMwBpiaiHrdFoIGQcvVULmKMOalpKElZXEnPkjCnMfmJs0aSyxAJRKZJqk+TFaxVN54hAk22YiSP8Z6IY8mCse4Bgrib7UmzSZwMZ2Fm/////////mZV/u3/95Lon9CBgYAIulAGgwMAAACHQS0YDspMJAUKXLCz4rLQihCSc66TiGDkJHNyQrqOU7V9qiEgIMpMXmfcZHYYYBoJ+mDQMcku/+2MhhqJcX+EMNgxGCGrFWbridtP//zyQwkEb2dyjqI825/zNz2naZzn6zHTPT///a97nncjqmf9VA+4esz2gA0IDvGQwGHXVhh29v9CyYABRfGFj1FVUI3Xljhg8A10usl4huw1JsQhBcUewOmGwItAk1hFVSaZCdLVkCk/kJyGiRAZFAcqRjTEVNi1StDqwLLmzwPalz/+7Rk5QRj6UxX6w9C8Hkrqu9hgrZRRStT7LzUwkgwKr2Hn0jzfmwNeYOWMI5BNUGbqjQyIsqlIPSoUarSzAu2m+M184+p4tGjP0fu6UX/////9nQqXZXP88inT/qmPshH+o1HhcYE5Bz3MMIq3YUAAAAACK5VIZYDhxQEvurI1E84hop+kUGqN8BCwS4BYEhfK86mNvKMggSNwuf5fTNZiekvUAdDQmEpPimWJqICm06+c1czqoWtc5gtECwGHM//7JQ0hQ/1/KapKTqX///4XHmWm2PeZ7ypVlbU0NT17Bk6NtIS2LrIzyNWbvjaROjxoSpAD36+9MSgAIAAAAAEU8OvFmFsSU7LZ+MAoc00l/VdP+KmEOUfDQwEgMREJqVEPF8pKcBw86zOkMRJosSG05qRoDOkQLgsjVQ95EQo91MsuHbVy6H4S5uKphRcEgaq6uiItUWLArlLM2fdsWvZ7k5VqBmmsf/6tgZVP/////6yoiod6OIkb9H51V6ynf+o+HEDhTvCcdNRa2ro0XLS/VlSQVdaBYpCLKkL0faVlI6Eho5Ucc4NJTvMBzvK7Rhvj7eHWvn+rIDlP47a3QlSPtUwaZneIdbOwcCcaK//28GN9fJohHqaMI1vm+CmGWvygiu9cXG/X4xjKgs1xsEUSeVUpaIFwhHMOkdVEDxUm3Qa8cYltLUYIbxfdkWIgMgGBobelExoKMkCCMEPKNCNMMva0dlriKbt40yFUjkuc/imKY6QbgzMuZE/EYSk9g//+7Rk6YZkWUfVay9LYJBMCr9h5bgPuTdbrL0PQeIuq72GCtmJpNXGBuprMnI9lnVwVMVVFWUzzKZ5Mhl+dQ7TOTrymYhlMOQe6EYeCP//////rDn19Ht/+znXp/YaO4OyMTVcMBEAAAAABYUJQ482MeaM8GSsCCNYrloltLX1HkEZkxWxYw3BZd49oRilsYJtSyCOBIhcz8L0UYZKLLlronZcyDB/HIMxzTUBVqqLlojgEG00G//9kUnECufUnqvXRs+lMj/9/abRVX6gkDoplmpQz3Nr/+pe2SqSdzzEmvbd+ZwmFWBeKhmsElrf+uuIYAMAAAAACReHOIzhJyz8XQcgodGrtdCqgUWMAHEgAaV6RgTxTuGnRjJfNlbjMCfG3fCj2QbwFk8DOPdmJ2MVVn+fsJZPRQHat/Lp0ZZ+tY4FZEYj8NI/VtxQLHiJBt1Rf+2sPHCLjrM57m2mMfT/////9NzThxz/RVmzjd0+jtzZvMx4E3H1a+LFukQghRDqrCDBJbAEAoorYC0gQsU2c1mwVeDsge4HQFgFB5DblUeSqWKhm3ftVkCfy+ELEhS37TQc5+3F32be9+1pqDglJZKYqzVS1vps6ANpAa///LTpIk+34qk6YXI/6vI3sPe5LKzr1TGKer+Q/+Z/2LJx+aBO+jKMZFKN7aSG2qyj1lP/yehABYeSOCBRBpc8zRuhVUmk9SgEHDjBHg8HLNw0LcTWV6qN8mjRxFVlL0Q2WVLtN2LdhU847roIeZSUHQX/+7Rk7oZkaEdVe09L0Isr6s9h56gRAR9TrWErwhkvKvWHiuEZyruOh4pawm/Ls5T+Q5oUR4IU8IEZJ6uLURZ1v2BUyzQJKbr7UjWVF81i3/3vyXsX//////+U1P25mcqT/m6B7XE4hmEnaGavipyCAAAAAAQ+k6FwgYbQceYRgE/DvrxYG1h7pehxBPAHsWKtiJQdcll1qicbdJij3D6wymjUxUCgCjKAGRUsQvR1+3zbaAVNRJTiy6ddK7Gz9cASGgfL//UM1R6T+HOekdIqm2XLU2W6ru6T+nG7Ub+erdW5vyYHlzVckGhg85D0ml1ZYQ6dtOV/ROjhljvog7XiP/AEAAAABJvOgBhrVHRiAbvyBASofE10rOTme9DVFdMlMRRRjjvO4j64BIJRyLRdQAYY8BdJ/XDgqSRZwYQzl2WCzbsxRP2pWr6gHmgOlMeXTGH2NRFMgFuFusTBrN/tMgYYxGJBqxkLR7V//////66/yfDUr/+y6tRyTSMsIY5hKx2joQKcgAOJBQQId45SYwApu5f1rKG7XCEaXhT4k71Sh37qSr1FYOXX/cEqiXldJdbftckfutDPzdqrGbAoKZzWjVm9BFxB4HgQguIAOf56HCMEw2+VSJ6aS0QRV96+avC0TV3SZBJdeF95lbv879yBg4hJccCnq3Ishpw4PLWdWkW9KwoADSmjglIeSOJU3SKaOBQE0nImEsxYLD2RgZ4m9pKHsTXxLhLylSDLIUN0xwSUZAJIQpRqh9w2nrT/+7Rk6QZklE5Ua1ha8H7L6t1hgtIQxR1TjRzaQjEt6v2HiuHMMIyWZx02qwcA9bLVynQ0pjSPQ+m+ScXUuLesp/Y8ylgT4bb7/z+54fajOFokz2k3+J/kf//////BCSFYx9jKW6CAoCLMYvu31d/g1EAp+JhduWBBABAAADIpzOgEQaFRdwLFui7Zjmg5VSbnRl6UBIqG0Vutwrn5lCbHpYmZOhrFOtAsWTq/O/v4eJhCXWdmGD88sST3f/+69IJNt/6ziwtM6Pfz/Nd+2tuoWbDf83Gzzvfe9yRBzIM+hc+adO5G4Wo8xg4+aLPb8pTmBgAAAAABkPhVos166reRuiYjGFMINet2k5m6L+kiQasysD20qdFRoQ0ABFYdkQMXAYnQ/rWQmAWJBLNEnwDkWnmrlxmxguXsruQzx6PigGFDqCMf8hBMpzlIhSto/T//////+v9rIu/+ydL/0VRMwiM0IWAAQAAAAAUsQiBo4mIFAhapSJABMRakDclPJvqsERMLiQaNcVtniaazWIpwM2Wvb3jMuIpnB6oSYmgkR8L3I+3+mGAtqaGAwsxY0JcIXpGsT9LX3//2tBJhTKqJ48XW3zSEV6SX+17mnOXvZSaSWOrWqnqUZwh/Dd+9o4oXk3UpGT6L5EQz0Ltrio255UWCgEdOfTBoAA0LS3IEBg8DR2CMOJnqMPc0gmKXiHTAUQyQwgTLLZoNJ6wAou5LC1bVD1LFugw7vhjCAIoBiDos0SsS5l8hnJ+H0EkqdZL/+7Rk5QBjy0dX+ywz0HRruv9hhZhSdSFRzT02wiwvqz2GFxmg7CWJA6lItieP5iitw3QySrPj9dEY5HO5MoZSUKc3oIZnOt/5Mq//////2g+GCSkSZN7peHXbRGfob16PEVZowPzqmAIAAAAAACzKwNjS2JTjfAkDHwTdJg7oqIpdBY8AhwtBY8pinXEnqby5ATytRg+C6LAYEPk1h50G1NV/ufR///JGtl1RQHea5ahlrFWJA1CW7AKDIehf/LDk8BIA5rUPNbXx4jdaRy9MX31PxQikzAxFhU5Tpz5XwGK00yJspgrjvsQuxGI9FerNG+dyH/uyI55QCEAAAAADqXGAhslnA6k8ioZUgohZAahiPagaJpb5ayq0QfUvqzaG0Wn3bsuNd7Kkh2SHOK6f8z4wlIXp6Xc05GDnrdOQIWEfbajRLS9I3ZuQxyhbXzxbFtmi/O/9/iIoHw6Ukwt0MNdNf////7/OxAw9f/ofm/HF6M1iG4x2PGCVA9GmIAAEAADywIBkAghDDBQUKgzomJwBMHKdqRBIQBgcDCYOEXOUpQUqNWZfG4WhP1WlE7kw5EhsLAlgS/S3Gdyy7rmuxuYDgVBOvxz7UaeKbcJX6vHMr1Ytf/h9kuDgodp7fRXeuWmbSubE6Yn7YYuGb1pzSmnDU5pq/rb79pQBMNRQtLoHoVZ0ybOjIscbtfqf/WBOKNZgQNl5O5mJpAwSSqiuDw1zspU/J3dTpeic2TOYm296dZpIYswFwYJtCMCsT7v/+7Rk7IJkikjUa0hmsIUsCt9l5agSkR1Prb06AcYvq72EixAdftiF2lY9VlkmpL0waA9En+ymoSDL0en1CTYGJA8wToq/S8pwpSCwIKOyv1sYmn/////93s3/+b//+oV9WDvcoeghdagEACQAABCMHMREVMAuHlgFGghGQzaFCAhHcZBVMSRFC4iFwge2KDh1ozpt86rqNMadJu4NlSHTJS7TIEQDFEOPYjEOWJfqh6h4TGBgkHYYlLDZqXUM97iP9Q81//ypxCGwZJrRfpIm4IBrdrfv9xSnVZGvyjPzWcyFZc68Li/FWgquTLiLjA+IwKMpNCYmJGWQqBfv9OpfQokYAAAAAZV+DbRuEk0HBHcgKmHhC1lmvAHEknF8YsRcCWPHLb08yOfibtvfInIXw38CMkmXLjA4YFJQu7NURCU3vRHUlokgsaCdNaZucgHaXYjCPyVcsiRm0c4Zf+VOM4pt/////9GaEA8Onoie6n9tDDs9H/rbq6nDxzEEcdW8IQAABQcFE5jS0EBUGkUhLXObOAmiwuaVwgaDWEJn6X4uOZjbozi3k+Go87cjJeFBePERGnJeK3Nfh+es1OZv4tou279JIqk3Ff/poDTyA9//yGAqEToVnrJNyTVEsd9//+O5vlmooNl009bymn7GHvy+cU5dNTnEYjWpMMzCIpNUBzqCwLcNaZkwA0AAAAAWG9P40jiYySFQLK0B7sQQquuYe8u1N+QqHQmTwA7E61iLM4lTAXWeQdHGV0N3WlL/+7Rk7AIEvUZT43hLcICr6w9pJ7hRGR1VrWErwfIwLD2EiuCZ4NIDKE3mJDSwgWcnonkiWFKJRpMjF7VmbaGn2xu1/6QFXJkUtrN9+4Tpdv/////9IeHX9H/uVtVL6zlYqLxsOIM4VAR1WFAgABAAAA2pYEEmRCCjjCR4ZrBzIprV2LuohY3gDxhJvY/pIUsyCTf/UaSMBkKgXFVHe0Krev6sRAS+qef6tH3+QJsQh3/sxep8VvsdI4Ghpia3/xUfOi9R1aryWZF66RJF4jEiCYBEbZNo1D6Dmw+YemTXJte76ngwAgAAAAAzO8n4DESkHErkLT4CQX8tgPsYEU2RJxaB6UeLCaSExhip2OYTKohMiWhuog3h/qRRNoJGjUwdClFae8FVPHidMwspwnwwf0MaiOOGledzbeAooEADFQNZPulNv/////rdReKEGN/9Gu++bzna2mZTmbOHCjj1AAAABYjGGGAx1BA/yBqaZ8UzOC2TeNhTrUPBgwMQgnR8a3qKTCEiRCwLPLtCFAFAWusTspls2YRR87qDsnBFBg1BAZ5o3D+cu335Ww6XSzKi/d7+2iEKkpioY6f/N4s6WJb//t7i/93PL2O6sk7oblrSK9SIEoM2haaDLjDH3tNB6CGK8D7RWoqgDZ3VMgAAAFwqn6wRIRWKGVyLZMvS9amSUDTB4mIwdPQvYHWoW6ppu8NXetjxERoakmYixBcStQGU0JlcQTrEcA9Z+PtHyjDCRjyGyTKREIQrBgp5RTH/+7Rk6wJDyEfXey9C8HxsCw89hbYRsSFRbWEtwiyvqvWHltnqVKaL7RRsxfGZKVfNUPy2ztysIh0QKSTyl/o+n////1ozVty/bYqI/O3jhxmq76C4uEi3IHgADaiCQAAAEFEgIIQN+heqQuGv8+gUiGiAEmesGgFVIBjwkQRzmVlqFWWIgYBeOuFEpFCHC2s5AkaJ40S13/5WwGYqAl6iVTKu1+FtIwgQmwu1id3OyAJLJE0NzZ7BMoSCJa00DDbd5FaeZv3wlGEbq6nD767oNqWowxNCgBolSvarLibEvFSgHlcS306MCAAAAAABSGODtYvM/b9VR9TCqUclIcKw4EgCohjLuEBmFVSqYDtV3PEKqF3VYXrjLAWLGJARlMzWYWvQErzlFtE8OonwFt3Q/kOCaVMVqsuMKg/gr2ic/DcSKoDZOFcPjoBzEPjTqlyximJI0HY4qjuQvj9/s7v////9ZBD67f0av7dNWddqkI419RAULsQwkVRhEa0O2MwwEvijo3IPTp9KhZc6a72LKboKsCYtKHNo7sBJUlUFAfa0RQF3Vvt3WsqdM/mX///SOsrEgMrb3VmMolQ1ILmw4Y96mjN/VUlMvLlUjpK9+pO2EmJ+z1KZnhKWeVZsr+ZGvWx8itlSNidqoSg/Lr9tUWtPKKr8knvaCADc87RxaKLQqOYbZjQw8uZIkJr5qURRfLjJhIYrrSaVI7SwtgrWpJnsAvCVEJEyeRXmhxwcjFwaIwPMMMBMEJq++XFQ+ET/+7Rk8gZkXEbU409MQI4sCp1l5bYQVRtXrSV7Af4wK72GFtgunCCV6GRUo2abQssrt37d3zJCjQwcRBgrHp9v///6IRG/8XuK0Jerf5V72V+3t8spQlRwiKhwWcwCQAAAAlhwcHGSgKMi20E6dBwR4KCT4sTUpKAFhwqHh3XaizzPzQWVSluREVhX3HHBGVUkgkEjPZEsqvM2//9v+Mni5bFZmeVS/RYwe7kQdNpzWKbm/xGRekCZPnu7SaeSD0uk1U4+5qeOz/2Vzh7qcPnh5zxufpsKtFQojGzaNZHdzio8CXmoGTd2pyQhDb9VyYABAAAAAGi8bEDbEPlh2zLNeAA2rl+omm41JHB9QwSp3DVpUrQEwyjU/bMW9h+fFCF9QeFXKM4GGzlTiVqXozNmfyeztQ+yJZUzdqU0ktPlK10RR251ubayB2qWgQDRZFWfNz8RItNKyZZ8tLXs4zf/////9kCxVEX//VF6t8La7R3OjlFR1BwRAvUIZPRxNCGacIhCs4yGZ0cVSLBlKFjNEpzCgAYJSMVKyh2cBqwC5gE4Mo/9Zay2o9MIoLpaGbGRmP/csAmo6TJRrzwFLvDihKvLGq2KJ//2fU5Q/v9bWg+gMI3K5m/UnWpVZ5yv1W18/q+pUFFN68Xoi78swjNQqewisajTClt9Wjqp1ABAAAGxOIbImqccVIJOoTI1nLHmnrDseIBtDCDpWBg2puuzahZI2jfrKYOrcuVDFS1Tp1k3GuULhyIItHr0LRPopfj/+7Rk8gYkjUfUY3hLcItr6s9gxeJQSR9XjT0vgggwa72GFuAahBZEWWC6Szc8DleepvaQrK3/+1r9M0o2tLa52kW5ekzPWb//////7qip9/39PU2vYeqyPRhYOiT5gdBFVVkAAAAAAAg6stAQIRQiBLaAQV2jyaFGEZUUWnjQ8AKTFKUq37Z+15iGccQQNfUVUhb3lLVvypO8iApMxHNT9Jj/0JboUINOGhGMB9jTLrX5PPFEl4S+sg//4k8XCw2/kyg+WaJS///F+BM2L+6P/aXtLi8F9Q5yutQAOYzwiRno1USI8XLk6/3fjSKRK2LinLw4gBAAAAAASVxecN3BqXE46jdzmhaDWFiO2lgnclU2FN2UpMqFr/kK044z9QVm0uUCGBlecoXR9Sn8eh9H+hRYVQx6MA5Fa0/a7OFCVXc5rKcpbL6qhRggJiguLAx3iHOwiEAtzOyGI2Oq3//////nIc53P6uba6VboOM9fM6M+rKQxtREFcWWRAAUocHkWUw4wxAYoBFAIYBGbsg4XGB4EylPY0pHTkyxAOBYAeelmkC2qOzb59YYY0941Jv8+sHwbUh3W/mVgC5giCveBIzMSGVb6YUAojF1hY9/+3ijJCg/8PH2TmEKL/+v+o0sl/D9La/916vaQ3z1s3PYJFUhQQk7iRFuRNKCwgi9TClGt1zvsAYi8piUmYSuZH1ZLtifSgK+obVmTATEWktNNoDObmqBy5lDKB5AWafxnKrEIVNmQtYTAg97ioQy2G7/+7Rk7wZkhUrUa0hPIIesCt9h5aYRSR9TzWErwgkwK3WGFuDk3RD0Jo0HqYxLaHUEj8YjJORCmbWbee9abKra/WlepJysVVjP+x629Mrmqr//////1QjihWb6/+3pU/q4suhnlGAmowXcVVWEAAAACjTaeIGGFYAwQQvMKFyD4YsI2JAYjiXUJeohic2gKXtIZbKKjHkSXet8+wl8HBZ2wNASACQfMtQb7WOppN0ElTPL2sDcGKNfe3XsQBoEQdBQIx/xsUwGTaEQ5+20kZUQmSHM/88vrrUn6Z/7Ef/UIX/2qLtvQdcsooySCsuA8y0Z6yjiUBF0hOCkiX/7kvDgIgAAAAASEwqGGBg4eBDLKb5XI2Elk70ykY2wWAQ+Zoh81lRtrSmcjRFoIfQxdBejwFgpKtlLIVh2uwezFWOfkdqrDMvLRGE1NZtwXoh5aEgSiGfpzpxlDFAO4OFgdSHLU8wkEBGf/I7F//////64kGlR3ep9X/O/RRZudiohWai0GC3FA+gzejgBAXO2GCNA8RExkJMOPAD6fyC7z6h5qaiinMSsxd6ozp+JfRf4tGwzHgBo1iHt04VPBiZB6edTS59Q3yUax/C/PWz+fOIyAWFaH/+7ZU5RlZmWeNI9/8o579s3ybPK1FsSRFRGSk68ai1HSkAmDgc3ylIr6atgMwADmbxhYaZSai72SuChJjKXlVtbV0XyXU9rX3agVmbxOW29K/TJW0fihYcp6RNZbo81MhFAQBgmCDzBU683ZwP/+7Rk6oJEl0dUY1hK8IjsCt9lhcIOyRlfrC0zQecwLH2EluAk3axIvHWhXMP8PlV1VobteP3T5CIiQhvP//CnozD//////+t3TKn7dtu++yDBc8i6eh9CuEhJdAgAADLjAQFGYAAD6mDCQoAnDyycSMq7FbyBpwKZ7KSDCl01WpfpXyI0jQzaba/64qdDOAizgCCHOZJVl9imXiwWcUDBumBkkn8bA4LSVzxrfUxfnivZys/7E5PjokW+7i9srF03vXyPq5f57z2zB1ea1v8eTWP////WkF/AvD0nlWwpJiTjaiDWQ7M8zu6ORThBHGiTugp9ESYARAAAAAFm+oaP4LcrVhlYywB9DEVUlKl2ssAwksXhdpPhl6GDAIgsR+ZKmO4bI2AtfcF3p1t1GrATgCiQHInjqSx6BgwLPqsPgaeqVrhOdfTgaVOLriIPIlOOTVNS238ICQTYW/ylld5//////oRWGDzspr/9Pt5chCiLPefuQQbAYREhVkgAQAAQAIOJ7hw4RgFUHAHQqhxynYcBBgpOtbxAFRXCpBjGSIUyngXvYphzFwhx/0ALcbBP5iaoS00dPYcKELKRsPkT802ZW879/62XRaOuL//FThdJURuaEVWKQEhN/fc/3Bd/+g6f/6tWazBm+QLFkUIw0ORZUtFk8Rg0HQ4SbnLeyoRk636ZQEgAAUVFbHlgVRjbXV7n4TZR1ReBLYhIpQy9LAvoGfSBSSisGFuZe6yOEgWwnOSPFguUBWJ0L1kRoDL/+7Rk8oIky0bTI3h68IesGt9hhbYRESdV7T0Nwg8wavWGHtgXHwkhAuVKXEEeCERl4AQSExBH7AQqJIjDUTjoHmSsOhyW7dDeu0lB4UhGi/WtHV2f/////+axQ913//nP9OhzU35jG/MPOGFVpAAACWcmQgcNIZMPWwgadSRBwshupStZEASWBGMBgIpSoKTMvi+ZwBCUon5vo76BRAUyBAPkJSIqGwq3FxYm2isMYeJcQBQaqlMA/o0TXY0iUxdjecP/+KgGBVhCshusbuKYgEixn/+4V3SXKttR/6O5eEN/jerUToBSmiRESMVkJ1gnEqEyhczHJgPI/F7pLBc99foeGABAAAAAAkXRCkRiJrhUVWl3kZASK19AaiYis4IQE77TFVlVm4I3uq2NS6FNAUuTsi7hLbFgurHmGzwIHo9BWI44lqhyYl0JSCjNS++oiPSurMnz9OTHpR+PbJjeCHL2msnDUiEwpTfqpR2Sf//////qa6j0pbW36Vbqb/H3/q7+NxwNUAAk0sGgTLS4sHkAIHBQDUBoMLhLA5FgDYqQkAYiN3WRDjjPtRgYTSIfxnb2bqFuEB0NKOKQZs1t5t9xm78XdhHZBADhceBrD251JZz5RLlotOmJD/+xZqKKx8fy7WzaX4HBpK6//OH4UOJRMfmnzV3/Pwns4pU3GYrNtzAtxMhP58IxUDTooQCc6xUn+qaUCMAIAAAMkvUaA111hQVteVVJR8VrpeQ3UurB4V1N2RQ67MgZZm+1eEz/+7Rk6YYEqkjTw29L4ITL6t9lh7ZRyR9Pba08gdIvrH2EiuCyVKoyOA4W3OehpckBIqJFswacJlGJqpp1BKjtp4aIeV0bEqc7nfz/ybOCeNZ89fY+5GT/////b9VASf+ns9r1z/YQ/TCM/IgAFVgwEAABAALNFAoAJiwYaNLIC4Ne56zrc0SFvcUrMGJXKRCWvqehbQ3slIGANPjsj3u4j0xybUmr9PpjlHz/oZ/rx3VKUTJl6YnP0Fn9Rmyo8+MC3v/1J5aS0DjIr8sKBCCzb/+XOUaWr0svLpXd8+39lV90vWRxhMLEUegaUI27wogEKsas8tGsVZHThAIgAAAAAlNqRwFoRkB9JJB1YUijgh80GgbArAou1FPWo8rHGpLaZC/rc2ZW3HTQECn3dlTR0nAbKVgOsj+nIhjc7PwBbl5IpJJw95oeBxZeyrUMvHETiz/afm/b5/YmEppr5+fnpmH5W9v////+rKRvTK9NWVRLsetlbWj/oaTaEAIOgAATYWYIFQQqsnOLCSH5xzAHCy5nLhsRgAEATOS12Ub2HLAqwuHDQ4AkAAhSx/naohD2gtzRFSZRdLtvXao1ER7GjwdwZQW4m57plDj8Qe5C/pJPqE73W/zg+jUUAtQcJX5CFJojhIRf//3NBQzkI5V3Kp7Wf18n437UJfIVIQwbJWwLFj6SEwjambWIXaoFxSgafKcOVbgZgAKx3qygfZbZVRQRNeNgkDA0QkwG9g1Rper/MoelIaFqbV2XV34a273/+7Rk6QJEW0dVc0s3EIRL6u9hgrhS0R1PDb02geiwLH2GHthudUWcS0ulsMTlSQSy2wXZg5bx8ub6Gxrlmzp5lhcx1nNDg/Jj77ldnsoDwfKBUTvPP+qk6f/////+iElT/79fnoTMtad+8wdIaoPFR8eVngAAAAACWqQmgBiwFHwgGGMXhN/dXsDAiSTrPQnKYUikWXmf93H9b940Ll20lBbyjAwTX/KX0V8hORQqtYtcmvsMNLlyRSDjyJ3m2sS6grASJgOAr7JCQo0KSgtNA+sTfAmf///9k81MyK/WqJ3/5yvlXcBUZQhCxnAqM0hKjbu06TKgcRqOvA0VzfP16gAgAAAAARLo7MP0USMgV1kx4qbgxhE4MQkIvMlM0pDJe4sBWVeLUa49BraAdiK6oMFAmVJWx3mQrrtLlq0syuOl+2sb9WEBT7WmXquSqgT122HU/mpzfLZ7IoylyjIUsXHpnNCHGIZ3Kln1F9G//////1KQiKfanRLcy57j7MaZnp1iDjC6iYACyakRAAFNOjpyrl3p+xRGh4QZc3YWGRZiDvw+n6xZ6oIgeVz9CvxyU6ZiX2ZcyxqVmFr4g+AWHkeDOhUACAQIQYDuOEhP9pOWUE3/6CfTpinyoyKQVUW5/9jzXhJaIvSiNtf22JM0tSnwwAwCIWOA2I1Q9SeGoyIgDXp7NzpgwAUzOO5B7U+bkPuxKhYzKk7WCKrzUeU6gZDmlukhCVm5QGyOAlA7TupVCkVgHRmCoHgyCkcCcVT/+7Rk5oRkY0bU40c2gIuMCs9h5bYPfR1brKzXQdQv6/2GHpi6VruMkxhm0aGsU5IuRuc2w+ns7BMNjPrs5Qeuhpua2yJt//////XPPs//+nz1LtYocrbeYVKFsw8qKjH5AggAAAAwKgYG2F7yqTbgWbWuAKLKkQHHmLSCkOlYGBUcWky+EVHjWyLALrZ4HsjoReDwkIKKS6PPhj3v/ffZTBL+S0UpgepDtblhIcWKJ5H/9FITBLWm4OUYKC035f/73XDkT1tOSgTS11fc7KRy8du/i7iRObxPzQolLVpmhBq8AEqn3XpmPq9gAAAAAATbiOJgExNMNlxbVwRuivRrY9Cwy6FiMTWC7qQhlUoKsubErEh0HnZetJxkwKQrpU42EaHC2vscXpQqpS+bo8o2ypwHQf9fDws6dGX5JEz8lmLTvLCSmgECgsESZR5M1NLN/5Hs+at/mvz6SLFb/////+rDw4UeHnoZelvWupERO99/QaCFqY40LGUgAAA6BEeN2QmFAIjAUORgAiazQBAOJCiegcEiNpsGYbALUPTLSlcpMuid1MtMwWvL2e2Uo9E1FsiEjgqOOPK4rM2v4wyKGEjcUAq9ZJkyFiLKfQx9jB0pHqs7mZmTKInxH8doMXOu+kojWdWZmaY46/nN/P9fKzvbeevfXNYQkf0Hs/aMymV0MSERfH1luNXQkJ7Rn2s+IPXpeCASAALbuJBF0WlocOvnBA9OBG1VKmI5C2nAchdDBI/BjOqyEFCsxd8Yepj/+7Rk8AJETEfVa0ZOsJAr6q1hZeJTTR1NLeGLwdgvq/2GFtlxUA908nI88tlBUqKy8anCTWLkSl8wnGTuJD45yNg8cxqFCIbm9zj/5MooiLKP/zXOn/////+yKOFmpb/+iaqjdGdlTWuW1FQBKWlQMwIAAUASLdHVDkHEl8nlEkEEhxPrxL5NSGQIAWCEAwuwLpPTGEj4ZNF2PKPj5KuLhtQuEXgfhfQVXY3xd04CMt5mxJsuVtXqmzYKjSP/rfzDePtpBj6mca+/lPhZFU8Ub0VLe2Z+6lCmdw21ZMSibJJUePQm5edpsB13RzRt37b318vWJkzuZeJAAAAAAAAi1h1Qlt6kEQogKJUePSmsAAbiF4XzUXTPVC3NLBJoqvSobGiG9SPcNKUl1kKzaZ/GPLCMggybgNvpav9iNLFqgKtEc5VMcgjqVD1otaSDsnjumTl9m4mF5v8rX/rwxgwOBg/9VKRCX//////WNQHt1b1/p5LLSQzqtul7sWJOHjVTA5AJAAACuV46aZs40AYDyawGvmjrMBIIwM1xvj/YxlDoMqVgRCFyHfDFI1/3qXc1KmjLT6nzrWr3sTJGoo/HUu/jfOqxV7v/+fhGa+NeX/tdw+tPH/+bC0nhZOouTjD/NulWLZxb9I4xDoSDJqkJxDNbJyymg0hRvmsMl1PnY/1w/0mDEAAnVOZ+DyUDhECHFyyUGtHhIKLsTdf2BVgW9S9T4ctlcRiqV1IoEvx1IYYwWBwhL5ibMX+dKRSR/oz/+7Rk6QBETlBXey9bYIfsCs9hhcQQYR9f7L0rwfswK/2El0jBOHfjlKzSWz/aWCsorFloxoApojRkNKBkyQVRBF0GYmceCFf+ZGnZf/////9UIp7tL/a+ydlrzMdRT9kVUZ1KYappQDAAAAAAAQEFBczpOCAYxpMVMXHkJ1xm/QMCFb1gxCGoQgESKYMqV0tNnbnRZW4vsax09d/Iwth92dTgjQlay9ekP3uTVanlqSyJ5a1hL26e/DHW27w3cgRbDzQn//TKMlW20pJNP/tk1Entjf62NNoWqzfvlf/v7OVKZ26aFNwB1VhGLFgoRlkbJK3c0ypQ4Asbu9T7L4hwAgAAAAAMA8UIbRiylfrUR2aOILU6masCRilDXhGmJLAM1TsXYnDOqEN3LOshb1prsF9Ue2cv28ii7LS4RCKdVb7IzJOJUakstDCskteudOxpLR/sZ/ET1NY52bTSUFBUaEL/O6Mn//////+zf///j3YhHUazejiEEdTizoLokmAgowwAGBAY0lgoKKgKJEUTHydE5bSwjHWWItlQ4ngeEs6dc6duBgAQVPR/4TF5KocpRHU+12p9xVmLb3/+ttpUgLfqqNNz7B8ByPpnSNUlCa8f/+hkbuqd2t/4HEVZcN/r2mG3zq5Q8vn//rfFdvxkblqkSdpc1EaPkeMYfh1S/Qud811a+mZcAIAAxq9qZKpW0KlRkR7lBAVmzS1Pr1vP6k6mMwRcs4rhlsANLgpmTFJG6UaWElL9KqTLclPBZsf/+7Rk7QZEwEbUe3hLcH/sCu9hhbYRDSFTzeErwf+wK/2EiuDQjqvQKioGBOaiVIEGTDgrZxWMifrtqst3/Ou/YpomhOqRXvz/NSdOv////9dvqJMK/opv7lTVjcxkGlvdToDARKBWBOLCVXiAAAAADClgGIgItQIxFlKcyTpziEGEKHpflR1R1zwC84EVGjGlU6uo4nmGPBRskrL0OPHK2ko0pHF9Viwc7G/7/s8ZMw102bVMNUkn3BKC5GdcN5//+u/HTd2fD8DjC9+f/tuhQ09Aupt5HHw8/628tLwnbTpE5IfgbNAsTiETj9pwnSBsGE62M/0fsBgAAAAtJ5uIkFCtIt/oHrgJSMBcVHpQJ+GeDgyI5eyWJor3ceC2VPqhLgRrrr4J+F3oEVtatG8CcThVgjLkERUCqM5FYqFwJQpKFxW3JAmfQikhgZbf5qzv/I/iZl0K+3O12q2v////7NVkdeVE/3/p9vVFL7o7K6QuoQQEC6gAEMDCNsCgYFfoLAbZjwXsmA0nxGBCQGOvGC8aEoKlBpDJ1U37l0wIgjEFHuU/R5WSahmbUdL2J8J9rpYglhh9J12ErREy/6ZcWmckroo7nicHJgCArCRX0zM0kT/O0Rfim3nXS0Nlb098zXuXprO5msW2a2m0zMz2w2aqexX4fx8xofWxSI5VPyokqs0zBuvuyLtHg8dIaKNhBlPAAYgAAAE9JOITnYyjrSE612xIta0yQKSmmUqLu+0KFXGsSaTQ27MnZlLn+p3/+7Rk6oYEW0ZUY3hK8H+MCu1hIrgTiR1NLeWLwdwwLH2Elqi+s20DIJkxAG2nCeEsbTmqY2hSVQLiAKjjCPRQNikTCEgYxDSe2/543yg1E/SzvUJdU/Fv/////trVBjXz/7f+jay1f/30YDjiKjECAAAAFlsiQuXuGEFzoAFgzsdECougaj+m2vELFy+byKBpyxjGOKlStpmEowZfMLyZI092AwOxw3kLt108nIEfoZA31UvuBiGk29qVSvT2x3TR//UMzVaR4nrCcdGw+iZ5xT/2qjpGaQErUk0Xinqn/9ZSXrETG2VkuYDSofoFVUE0UVEx1BbQlAwOjQ+DPtG1WQygJgAAAABcz7EQOFUrdHRf6Jh2mdPc0zGGqqtj9uU6jYHGkDmKfhb/6jsRf6RTyw6xn8axDAjxGQKyLIBkZBtDqiMU1iImXLTLtIlosaNxLJUWXo1XPDGvXRz7P////96195xE3///9XbuhlX/qdaTIyUGAEAAIARYEHTGwhbSs6wQ8Gr6MXry44BAhInYWocYuImPiJrGgUjgoA4M3KiKamY9R2Fo2PrL6TaTPJUgcLBbaM3fgh0WqLClrkbiwxOh6KF/o01+f3D8Zijdnfd2m//QJ5KVHHRySW6oqGqf9V//Qo8YCaua50XJQdDP/U6W9FQ8S1BCwtEuKAUHmoSKKnGBSiKmqqUfWe10n5gbBio+5VsIAAAATDplmF+o+hZNuxIRNwvDZbC05vC2hbBJZc5bpB9212OmHCTr1Fv/+7Rk6QJEl0dU409NoHMMCw9hJ7QUKTVPzeEtwggwKz2WFxBVgXjGiFWpjJNM6dZTXbLqR7Hhc5vmrMv+NwroUJfEkIRHsfxFgvLScfmtdueBWg3ijV0mvcYyi6fzmdxIRX//////3Id/9Slf8i3VFbUWQjyP9vK40FLVp0ByACAAABK90EZQVQiQ7oI5O2F5gceChlIsVepry1GpQ3TM/iH3Xqg17ijJuSBUsNiQ+hSsZRjA4CYsKoSHZF38DSyYr/+uuv/yyg/71j5UwlBZSZedbuLN/3jnc9RnlNl1kbB9A0bvDfP0VAR+TYrf1IiXO5c7UtNsgEYAAAAAW3PKA4b6PjKpBoWe15g66mDPbNoSngWqstNBv3mWgJKg4pCqQgnPgaB+TSxEvXC5OTjhe3dg6Kxay6ZKutSO6HZpe9khCAgNWYhlV7iShx6fs6GLT//////moV6Mv//9PlnORPVyGyORwZHgAAEVQMxIIDAsCjZgoORIwjFjlONiAQAjxGnSgGBoiDnQFKwqAGHAK2Fl0sQCAkMG1MC4w8JPpZUPZGvhlKG7NW6oABoBvbjlltm/VlL9oIXcgWab6zBcK7cbotlMNR+EwnVshJKD0SFgOrhPxoPAE//5KaBAQPLp5GoMo2H/0LGrK50hGyY5WleMyJY7k0JXuOTFUtE50cRyhZqCyWnDaNyiT6t8AAAAsJXjD/pMkhoWGOkh+U+jLIbGgqWqtEbk4Ehy3C/UnFhoeFjTpa6CX5UCfpizIGr/+7Rk4gJDz0rYeyhM8HHsCx9hgooUoR9LDaGcghqvqzWGCuEl73IfiCQ/JWgLPm1S44MiCoL5ZUFNpmq8rEtesLadDIR79zmeWt1vfP95b5Gn+mZg6etrIYv/////+tzgArRz+cmvZXuglt4IZlInUpzu8pxYUep1CoAAAABEOOoLGUp2a4JwolnjtEIkKgC+FKnIFAAjIDwaSYOM9+dtJt5VNM5mN0UIZTAT9Po12Nytx+/cv5IJwESeDw2W6ueScbD6JyCJrVjRSVDRBBx3+uaojk3//3aRUavi+9qtrz8c3F3ce++CSh0fFhxiGJ1Gp6BI22r+9ZV56p8BdFygGYgAAACq3eK3AYoEAQo0z6nLVumqRh0la7L5hoDXX1jLqXdt5AcPPxbpoeYWBO6pShs5S5uohQ/Q/Z//tzDGvPElX9Vsw84rXEyK+b213kCQk1fN4iKl///zZIPtZBBc5fUSZvMag5YJAfzABAkVLDNAxUgKBG6CoOyo7ZlDhxNJAe4yCYeBwoQECDCgmCqxp0sbisAk6jTOyl+oETKJVNdkragIDnNnVi7zvzL0hRy1lbG72b83F+40NIwdnj6RtxaWnrjoqPxJhCdIN2Mdt1PJKz//+/RVhjFZ/+/7z/14Y+lmx426ypIQkBhAcVVbwhksuoPk4WRtUzPOQ5jDw1YtHspzABAAAAAAoHApbMuNVvTIcRjsPmSOLCCMCrcrtkJbVL9eo4RLSJNGCBMEO4YIVI8Rxui4DpEABiCBpQf/+7Rk5AYEMUtVa0s2QGxmCy9hhagTITFPjeEtwjcwKv2nljCRZk+QtUMRC4ChOtUCSNh/lO3si89Li0uZ4F7RCkRaPZnqlcjfdYTqp1uNfOvkxAkK/9TjkCUn/////+5XGBxGtW7Iv6voj/2HrrR6Fy0DsPpqSCATAAAAAAyFWJCgCBhIFBTL0I2BnBjQcFJVjwoPA90GB4OBkIVfvWrc/248kCEBePN3b1O3WTt0qiwO4oZogGf/CTxYgg4iwworAk8fytq7PQflkNeWyySyFIXRhkneVlCBEqE//1aCQ5iXf+2uv+zeXxKq7veTZcaMKy9UlnnXCTzeR0zcyhHr7K2uqpnFSEAAAADft0+TcB8WqtwbFHhDEWYW5XWoNTJtKqxVeeKYLusvp2hvzO0EYfZlzIhCTqHxoiwwqVjI0+AtI1iyOG2vvPxJzBRsvbbGh/tHaZv+z+mFxgE/3VxAVKKC7f/////nQyihy7ldMj/s/PI+8hjVo3+hzjC/kTb0OTk0QgsCCkOSkbT/gBBxK8KBpegUkIxAbQO6ahsvbiBiPJGxf5rC4/f/iUqLD9JjteGwpiPAWhfPv/jRkJkAkLDmxmkd9V+7YB0oEQDofSSJ/4I5MFpBmZPJK1m9cIDBZJf/+JOHx+vN7/3f/uMErMS80YrR5MknCKdUFgfzWrtd5gqiIgimzng8Pcn8/rvYBAAAAAbLqSxemgChTpI1vWAZF1ubAi9nDiCbrcwucmdAphkl8sRIRkgFIWEirwT/+7Rk5QYEbklVe29doHmsCx9hhagSRR1NDeFrwiCwKzWXntg6OkCSIsAlQigmqzV4WIMdMqE4FQfp4ElfK+dneE1VzjEKGOjG1rbD/UrhVgQ2jDfeJt5vjKlAWEf9FOHC6ob//////Z5A4t/0T936yHS6XfZkM9kMIlSVkxARAAAAAA0FA4mYcZWHQFUMIvme8uLBSYEtBRAtm09XZMEhEskcpeeZWI8MY/yDByCSNoDIajQeAKX/eKIogOz470Blbvgay4eDIf1V/+nIzbVv/x3AgLud//nVRCXtt/zsv+NtW5Yte/fhpyyKKdEVzsQqnLAK3fzHPfKfBAAgAAAABbM4BiDS5/Ey3VdCVAQrOqNtSbu8EtT/XuzyYTFh+MxBeeSmcUj7XnrY0PokBSfg2PkkIfiUUTzHDp5DI1Vh45ztB+Nky/mj5PQSEVCwHBhZKMmNAdX/6EFu///////cwmQ///VH9R1eHSz/zd0Ezp9EAMGJDsSVg4DgooF1LxUDOmcAwEQTiQCpaFwQSCBAWiwgWgGgNeaABmzPFquiJBGHfmGAuQq0RAjSlg5fAbqNv/12USpw03UylamvKGy6AL3APgeEcPACBqv/5FOjhdQt/9UhQQx1keqq35geMyIw+jN/L9t/xXEQbWYtL/QTphGmJzYCBFLXYso4blZcZtRkFPRKVV+LUggBgABMGGGnGRIsNaM3rKIqbUkhPa4mIChKA1ZyEsSHkAIyQlPQ0IcWEpoprL7LlLWhLRWAAIP/+7Rk4gZD60dV+0s08Hdr6v9phaZS7R9Pja2awi8wKr2ki4iHCC7bTSYEq+JQ7KpPIbE4/LTpQudxbMQfaWum7yynjTLYdF9xOHmj0dguPBQTvqjSiPLzIGBC+P3w//tvIiP////+36oIuV/T///1HurfVyewpRZ+jgAAAAGEKP6GAAUFEAMWTFC9sBy6ZbpRpCJs8ZXsFi5IBGk+o0jhuCLGCXumctTCiyxEYHAMJQpxCEF/LgncUlwr5j0w0P9e0V27dnD9//0wIRB3f8BwEZYjuLkixUlj10DpG/mH//rm6WB+QP3LsaNalBEq0t4gwISYsZR7bbAtl0s9UCsQAIABPWbv8iWuoZISAV1NFrVSjKmvq6eV0WiNOZLFRsTmWzzBFc8taJasFC8T6Qqy/f1sa/dXltzsvE2dnUR0rmjUD3auWsGajX73yeqYBzig0uyaNdbr/////2/qepG3vR/1MfV/7I/6TlpoNUeIIAACxCBgYVJAJ4W+AwWIAs0qmQgQjIglcY6CEBqYGNiURZZdL/OhFqJQiWr2m7UodBhBZxEVmLMGtpAxByqn/gmU2YAjgm4OAei9QO/Lf/USS9gdaDnzH///RYJZDh3F0dmlFmlEaCUnSyW1mI45/77X//yXT8EcE+qfgUbJQRTggJCEKo2bJMWLEjyNAqfINXip/3MthGfnSqAEAAAAABoTgIEDDRRsCaSjFALvJ9rcQKQOTBEQyRjKlkoeQKr+lgF2nOYc/bsuoHBpuLpZWxL/+7Rk5AQEIUhV609DcHFr+z9hh34TTSFPjeUtyi+wK32Ul1BdS0njhqfl8oh57nEm6iqjlurzcQlTzGFgUAKsOuIzXNmELkaEd7vLzqazGDUWkppRhcI5tsn//////QwsQiC5m+36IVL3YWOYWI9HPbGKj804SFK1AAAAAABIqslLKLuQLWk0R4hWaqFsCl9KrghGLhCuORBHWyHnZIn+D2224bjvIPdSK4EmU0phenwwqfZ2JlXRcOG/+HI0wma+Po0ZJXErUEC4uKK/ERHcVknEe/mf/3PSks94yILH5sBGIQHn3ql9iGWEhA7drR3lodQAAAAAAASN9x0R2urkbktjo3WBG7N41Nr6ZamTE3uUtLYggnE2kJQoivJewDuBGgGZVkjJOPMlhto1bZIiHNMSx3IVjyu7rUW8RM3mq8Z57xtrzhF17//G7ihlWdHYp2IDKcIcUI//////7uQtF/b/80TY623efL0bU4EhQICJYcQ7KUiMgPKCAIYsG8Jm+hftTRPlBRHoDEyYCJHi+Kh0Raw70lY+yhqeppVllTFPVoZIEXMWwZoxkEir2pEW5iGCbhBGzLU+n/8BjJceBf7uH6+HCkTSd37orEwUTPOVuP/VhUcSkKGqgj1/z7fqu6o2xKpTs4hVb0lQG1mqupoywJiGVMxXPMKhDCFJqXpeAABUDxIibCCS5dJ/lis3B+cNs4SsYWsGLChYAKCqUGSCW6Wur2H2IR5R+VERSmao11gZ0SIWqicmKnKcKED/+7Rk5AZjykZWa09DYH1sCv9h4n4SVSNT7T02gi2wKv2Xltj/W00zxVjEQQ04+mZUKzKpdpMtz0mDEnFOz1c0NQts1Ep/95ugwQArh5y/eaIxX//////lcRZKP6L56u78tD2EGj3dURVU6M7ChRAPtUgQEAEAAAAOBxwjLgEaDBA4DIhSiBupKpEzk84y6zVAqGCC613ZORiRq4CZZQn390YzZP16EmFYa5zvDqjxnDr5bDTJSiivnhOdNz6RcQGBQ1H9Pzh9s3/c4wIwGAUhD7De58tfoqfWurtZGs+Wnty8/5TlHaKdJe54SlkMsyM0aIyiSjGsqGep/qdRGiyAP4CkAAAAGw8l4ZjsQU8qRr7Zjoh9mxw2WZbyBl0J4NdqIRrB00aVc2JMWo6Nhoi64BVCiYjm15+rcNuvAUDSfXMJTwm6sYRQMDAjASQaBEIIdYE688lC//f11MCzkXrP/HZzVYrf/////7SLv/m79Pvew0d5WaunoGIlYQAACYliY0HKoBVRNcvsx46K4vEwthk8n0hWIxjOpRN0/CsZwVYagimKGqZ3hP05oSJDTiVavZMS9EJQcoD+8VTPdzUKjTsXEMNBZL/5oSY0W/TlZFRGJtJH9S1KbU5+rLz/9/ck3yO3gaIzDBxYw8FIeE9ZpILg0Hwf/jtrZiBxo0W/9CrAAABAibS3FzsskTF2PHryx8oKAxwGBGiAFIrtLw1zDCUGwFKyaEkDFQDBGHQAUrIAcOagQUjFqxqxVyEpBOX/+7Rk54Ikek5V+09L0HoL6u1hJcYQ0RtXrT0Nik8vqimWF4HQWpFnmSPbE+cIWvA4QORCIWXpevxWJvGUyF6WvvtLmYuwrRKqEHANvFoEmHHkk6utYwRUVARaH1y0iBf/////9RpD3T0/Np949FUQEwkd/b16Cyw1bDA2ASAAABI/ndFujcjCDlDWcPIGwsiQsMcNNZgSQKArT3J0k3Klh9I1RQ66a1whzgXCPRQUYYlXfamBZfFCsRIF7WX7GyK//zdq6/9djjTgicQ1luLGTLbncd//x+kTAuaMJuDDTRDEI1CseJr5PHAkFwbGyHiExXDDb47qWlmzADAAAAAA2rwSwyVGhIKRiB5SMMp03kkEjM3TQl4KzM3YBAU2+7+wE6zbPIzp30vWXNiay1KXRmMYxpg+NymbOImycIQZMN2D7KM3LopR9pCsGDBH/69Z+EerK4t50JV3/////6N0VTTo09a/87yKyHdCUui9nOkkg1aSkQAFLS3LeKlTmS7AAA1MXIyqCtyT2gIcEmOHUKKIAJcWDNpTTiJKyI7FpuXwGodI2mSkUM1tXr/0Nm9TcjSfaVRfNtpuBZTEf5G+wQR2Cq/4oxIeaLz3Nulr0DEaTlXrXxbVjx5U6l///3+tFSmubHF0i1NR0opDpJRq2oejZtS6RZxF3/GvliNrFvAAFCWWIE0QGDPXA7whTtUkhXOmsgLLUrzfcICEQIjhLfpiULrcVhUvuMBjYcYQqMuByQcAuou+fDgd4PI/2dz/+7Rk44Jj/ElX+y9C8nxLyv9hJcRRZTVTLeFrwi2wKvWXltgMxXKIQzEJsThjq0PxXF1dnawkzPBJRKN+S4ITe0lYe73/GMOUeYxjd4xFUz////+aQ/+o1BhTE9dEVqsRTUdmSfTW1FIjo+QBQ8MVhyBAIAAAABG5gEqDDZguEnQVgM9PoR+kHHJpRPi3hPkMV8c54kRiQR/KJmrO84tq6R5shyIdFzXHiNagUo+zhfS2l1RVEBCjRf/3puCa+fxguCsAX+I/kwhnmPj/+K54iz0STVbEIYZARh6QDwuRdIphAKJqFxtn/13agRAAAAAATMyEodAgEJiwWqSMmWgQBKlMFNJ02QI8uGsK5KYl9d7XZyKxWcWvDzEUXlAlCVKlTMRkghgTBUvH758FL4jiS56YhLo2Wx0QYOUQxxL/NSEsUWo9Od8+swKPbRqvM10/////yJTsxEVBa/9C65E6sTb8x6X+xhZq0YAAQIVBQMIMkSjAwQBBEsOvbyhpAiGLCIUlyJVCwORSoitcRNR7SweERCFt2uP/H6R3GJkyMPhYMYARMT1kUVrG4cg71ajiwC1uKsUJLUg1s+5k4fpPbb/+W5nQ6M0KOOsN6xvOfDXb9u1///8Rn0Pesemra/+P8f7dVlvE8F5SIyz4drzWxjoUcXeI0VYRcGNJNwiv42lbhA1LwIASQVEdIQ0vcAurJcxbBvTuuViCEWGhlFIdYNOIcET7BySpC/TEFiois6bMqJpzvDqhBKnUmGJCMSL/+7Rk6AJjzUjXey9C8H8r6u9hhbZTfSFPTeXnwi2vqv2WHxGA35VtTfXTEX7fp6DgGplK2QZCW4ORmXjQl3Jy5cdjyNDpQFrazIILzOfxIDy2hb8o/////+eiv7niUayH1f//TehuPk3NdGOfPQ9DNx4bRa2CAAAAFFipAUGx0cDiAEm6XjOhSSBRHY6rCnG2wCIiwRTKnbavNmwC9IEaJ7hd1jghQkUVLBiljH9E3vq6bLQD+KEt7is0nVzltAwGxQTV/iqHDoiT++b0keJ1+L/jyj/HnWTXXF9VJ3Mc3URMigsPSzrBOEOQ4WCduObHhj6M+5TyQEIAAAAAHgqKHh2iPY6AxNxHxO2CGUt14OOuEqBsfacykaAbxeCP7Ay0bIC8CgL9Ok0ZDcDII/qkCB2nOBPStaU4+Dv47EYrxMfctAZuYlI+PFVRXVQZmBSKKoT6ZLzOTuTGxHUpudSDpmZ27Tf/////T841Hon/6K20Q90SXO+zsjto4oSWFMCBsWhckYkk4ZZkKg0MWBGfjpsqRSubuxBG1HeAQR2iYDpXBNjSKdjJtHemiU52xBdimNR/JE7bF0XMQ04VGg48Cq/f8Iw/h6//zbWSOPYxqAIIEJLD35LU1WhPlx9f1pMlSP+Y55EA60UaSPi9mLKAHMuLYSiowf/xHzqZJa/GASAA2Hk5UrYBYE2q9l5HwCoAg0WzGAFb0OBe1Vdi6oFBlrqcrVYZ1nJd5MRvmRjL60DBCW4jTDmFaFPEjVA8zdr/+7Rk5gYkD0lVY09EQIfsCs9lgsYQAUFZ7T0Ngh6vqzWWF1DLRaK3Ovbr4OhmtJdgZiOWz0lnSg0Vrh9KrdmNtP7PwVoVuWRXzs6k9Lzs3/////L7lHl+1/t2fpKHOJDqFs6YR0dIcFyqlYaAAAAAaFrGgEjQfEiCD67WFmE2WkQUNGdN2KD685Os1tmsP3hH2gFoGwLBwPbiwwCZAumlYy8iv7DcLP9x7g/aZC2HerWn3p6PjAAwBbx8LP/5qqNzVnmQojeSGxQsQGVHoKRFyID7IJy8tzKR7dfwUJD0kaUofNN43KMnELq9RuxcVqbWxqIfAuf/pn9Jn813PWAFgAAABw/rYFkHZZ827V7QuU05mjAF8v0PKJzQy4MWV+ow+jMnFYlFWPw4xFeRal3Vh3Ehp/W5S+WS5kz7Zzl4sxZIxg0kZiIRGbgTAuDTCiBgpAjjLFv8z2Z9DMFbrc2/9YbDMf//////VijNdisoT1WWZwjb2ncZlBldlav8MFC6cwQU1srs8KJEMBAgsRdRgApLLYiRIiBOsIwpfNtQKRNUIUa9XJikGP1W36yO4UhXKglDKj0eivv5fIY9FueHCp21W3n/7kvNy2sf/8baWs5zN7jAdOUeNP3L5ZDaHjXqxo+evSjyA/ahSw5FbgSlCgnAlTDZIEhl9mjTgaVPBchkJE/itN9b4Om6VhRAAIAAEw8gCLr5KV2HPgAN4SFdlk6K4WQY4oUIBUqEQkiGdw0/KWbSwcRSRJHdYMVODoj/+7Rk6wYknE3Va01OgoMLyu1lIsZRaUlZ7T0Nyh0vqz2XltmwEkiuVw4wdRKCTCMHMcbCmVeNhDkPfPkwoDxhIjDO8JOhJjOKomhzqFg281Sb5vvBqBQBjilIysVDP0//////1Ud/UV/+dqo6srO8s3yM/jTjFzlAIRAAAAANHBsbyAoFlrMVqsvM3CbUdfKUDAJadlg3yoVemV/KR7EzQ0IxhXTFCfRc4T3a7p/k9E+ZorqEM0Sd88c/xQHDiRN//LW1x3NbdUg62h1Tq4niPuqqlv779szurLd0h1iMl4dyh4NGNq4tppf4+KSD5gxEqBgIAAAABg3vYkE8yg8AMwg0BzZAwJztoIocX8oJD6XMjk7XI0ripLm5OzUaEVRJaMefVjEhhv0EpAiksYj88nMbQwwH6IsvISAhE6x9H+jgeWCC1n1eaWdI52py3//////9C2vrf9NU1a/+nWeeldbjZvoKAAAgFigSCRj0Eo8wgIBD0nDwb1CQERQPQwCosxokLBiIULBlGVyudMXRooripQIs5V1loqsaekGB4ylHAOSv+lS3BSA3D7grhbSqHKr+RjJ8aJf1n/od+ohA7bhsXTgvaS5FrL28fCfJirf+bOMsj8//6UV9Ma9KB1tohkQq6zJedxt6oMBhJZ4dpRIBGQKVPvwJAABYdg9QdmKSBe4wId1zkLo0X2hgvuOglSI/GACEwEOECMQxx2o+W3ZusOrSjk/yhgoABgEDBFXMBVtgovpiCgOpXIJHpJ7/+7Rk5IIjyVDXey9DYHPsCw9hh7QSWRdTrT02gjmwKvWnltinHaliqh6vk1c1GwMxnN6MNZMLhXqtxYTIXMS1rfP9ACYofUXejeikF6//////5EFXfSm91N3Ry2kf0I6M/okcZ91FBUdVWSAAAAAAAASJGNBGBPQxgUuMAjKzDttkL4JQEM0FR60gQWKIcYpTGYj1JCbnQRwghHWfkZVqyvqRVKSQv9tfG4RrCHhhq50zLqLneWOhhqNHOv+Sv2I1/7H1Jmm0tWpl/8qGR7rtnVf//DH2+GT0isQRmqYtVs5cy1pqB82H8WXACzzD4sYu2vBAQAAAAAAUFxKkTlI0tFg3Jf499ctlCZ8MpSK3prqAMKL1s0Q3dClVmfdrCWj3sITtMJRABgm8L1DUAlmBRhUqNXN7U2iHq5GK7t85/pqGh7AqlBlVL7tyVrK3HjCi+X//Wg+FRhmSnbOID3N//////WosKGk7Mq2rsZB+jmvyPdWe6mMLGtFHC09oKSUxAOMsFBgJFFYUeOPGdYqhIXc0mTp3qBoME4NFcnsVjhKZScy5JTcEc00drFJomZkVr/9Fi7i1KhD22NEiup+4tDihJwKj/k18Of/+XcYcDF6//cwkfvLTTV//VnmSh7GDGYBxpYdB6IwQHHV9FCwyBDIodEFZpYDd42ue/66lgAjAAAAAtq8clBRjIDMIY4lAzEEMMSWOiLGSUBLEcFa6tpz1gULl/P4vW4q1nifbOIbQtaBwAx2XLixtDGS47LL/+7Rk6wYEP0bV+09bcIqr+t9h5agQKR9ZrT0NyguwK/2WFqDI43IM5pyvTN0iPUviGR4PXFJ0zUcxjHz984YwwNExUrKzd4qd2//////rUqitfm2Qz2Rn7nXnVbox2ejfMcegqowAAAAAAAQcIwJDAwMGJAJKpCoQAJ4Y4s1TQsopI0zEYCGxSRGuKqDwI9LxiZWdDzpDEoBfKRgZAsF/Ui4wxRtEbJD3+8ZQ2ISg6TcoYlLx3XcLsAcdID46TQ1rUY40mCcTq/4e4wTCJovW/3spaEVms0UqbX8silUzhoTj5S7rLTqJJLlDx4wMnscXWTxGbB8OGpJofoM2EfuAiAAAAZS6gyy1S1WBcyMLoA2OcZusZ9S5DQ0P4YWYw5iC14lDio4aYG8kSuKalQAQAJWt1ac/kyCYjH2qtoc2Bg+7OpLRvVQfsoGl1QnMy8hGbK797+it8DyMpHDV4Nzr0r1OqZwx//////0yHZEm/mV+vu3q1FsS9NryDnSKkEEABS7hZ8qhCJTLEloFDxAaFHrXbbMKDUMkhS/C9qqCXVJNl82lBgRt4pbZcMdD0oGVMTfhaJwK+Lv+ROAsC2koQO1IXEwXW+4p8/i/oQeDVqR1AcYmQkxv+XU24oROVc/qZ45j5oJ9P1na/r3Xrp1/FH06SaRyK0KBAKFRkjcgtSEDfgey//8qtSBhQf0f1aUEsAAAAGB+SAaBzmurzRjuhWpGwVJTUgswVE6UKY4vFwjHGf994wXIbqshxVKIIZr/+7Rk7YIEyEdT63ha8H9r6u1lgrhSMTVTjb02gjawKzWXntiDBDLMDBEfVru2wc6jQJgPyKad1U2XkjxJWIjCHOqoB7IxItBI5qgRGcd64VjyHEnz/uiGlAejCdqNqnTv/////1UfG2+7+s1Fsc3o/mLU0mW3G40B2xj3Jg/Go2poMFERAAAAFivZ+Cik1S2z1pAUp2gpLJgRLsPl3kuYKci2k1hNQjf1CiVN2CqSaKIzG54r//8KZ4kFA0OGHdH37e8V6cgzf/PeHZVf92Yo0UQApz0v6tUrRbttE3v9/3aMan7n7f8JFpZZqOTCs52igcwQeKENIFi7d2c9lUYIYgAAAAJXcOGEMQSJtH9iLwGBrdEKoDTgYIjKuqKMzhavZuSRZw7K7IBijpswVKyFojsuxej5GoANAdesouIKbXXKTBElQCMStFWXoz8w4BBo8TvQtahxR4MGkNVvqp/X/////8yu0Wb/Qz7kZv/L2XVxIzvxoxdYQCAAAAUMo6Pg4vwGO0YobjBxFSlb7ODDOQsDBgdUyq78oevoNSFxGCBSi2iqslgQZU3JyN9wybe/+Z5BzvZCaMSmfbeu5vAyfja7Wdf1kkiZvb145DIaL//nIlhEXbGk1F/y2Wgo5EYgQ6NFuHthyOJV5s+IwWCdRif3X+v95Ivfx0w4CAAAAkpSrINZCgTECAsuI9ByxBYMFGqQtNoNCjBjKwwVGolGXUNEyVQJsRghl7kaHdiAouSDIHF/kw1KpNbia8cFwe7/+7Rk34Ij40fX+y8zcHmr6w9hJbRQZT9Z7T0PgjQwKz2WCxjbylMUKSBfwoDosmaUWCOw0iH49Eo3Qko/CeuvWTvpn9ZhshOTBN7bN6cd6rL//////kIFRQz93+9XVSlV/9EQio6svfkUW1W6CEAAAAFt+kBa1lrAwZqKCRjR1zl0ValjP8njGFvK9QkIcGZ9AQbJU38sOxsGo3pFmPHZdb/9RglMgBZxWCBFnbBpNHn//zYst/36hU8sqSkSme9/yVlWb3+4SYn///dQ2/i5qVXV6b1ZAKy7yCKBYhPBsUpJXe7raX/8qWfBpkLP6/oCSAAAAExMSiA49dqPT+KiYQeDbFl2rffdUK5FZmzNeHk1lIqsAp3VacztCJJEvWgwlQydBMqvBy8675qNQ3CiImqDsvFvYDKhRUDJ1sDy/1RdQ31hePnE7lfys5k6s5MaR/05+TNercxzf/////7wQNTGf7/Wystyv8qocpTPe7XxYEKUdQAAACRuWSUFGMmBBM8QQusZ6cky6qfMDxIGgSwHKwa8lMTSbMzpxrL4g1ahyg2pE60CjAmEYwHR/+kWM7kMPJCGSKxrLDvCtYlSq3Tb/5NMiDP+O75U6qrnxtSeOMn/lWT//iDiZUa/VweWI48UgapAQvwRIICwnHoPIrg58M3BGHNvfaQAAACw60oDKmAFwXJXquYJZFqmcRsdCFAkFBCElUHQocwBhF1YGexc7AwSFQsQ9VSbGARyRyNQwJS0TEfp1oBVjUrVtl7/+7Rk6gQkGE9Xay9K0IYL6t1lgrhQlStXrT0PglGvqrWjF4nQ27Rlgq0rDowNEljQ3GI8lq+z81HnbFG4XGSCQCBIELKSzy77lonm5/WRLl1RQ83//////cROLuzNshutZ3KaUlNbZVd3LY0jIoiLAsTZBBAAAAAAGogAZCEFgaCQ+UBUyMj3HAK+hIPD5ckVCJXiQ5Wxfy+dRmlkLajRW4/kWaMoqorLJc0xyyYLMOVe//oLEHww/riulTZXbl+tfo305PQ53/iRMc/4XUKOo1l0JKxVdqpT+o6mTJBIV5gsklg8sUQH39K6QIxxUx+RbRlbYdgMBAAAAAOKduLlQhQtkIMGmxOlgC+V6qwLCP2X+d+SpAiMBwWlarNlcFiD9sqXcXSo4McRrqIXbPjwShqPXmzCsa9IvquN2BUfBEarHQHc8vJyNjWfnFvzO/HqXYbRTZ7kLttNQy//////90O5Xr3Vdkrabkn1RjTEazH7XIMBlFa0QAAAouoZAwUhPAwsGAAwE8wNoJKAwQvSGWfINrUDfQh2iNx7o4piDE1M+ZeIyXsTeKPWcgjE8XX/wpBSRfIq2aSv4++hS0/YGZo//+YIn/11XKLT1/DpUek6MlX/7SowhBY9vxpgvrZpIeAqW3Kl7BsJWm1ME5Q2iI3YttY2SMAAAAAPBoIBLn0quy+PuMdcOHAkxlpJmuOChCNwkJRMQcGEhySLqgy4F8hYiCVAm4ZbwO+ZIraEmraLkPL7fKHvLAdekl1K7T//+7Rk5wIkEkbU60I3IIJr6t9lgrhP5SNXrT0Nwj4jar2sCfjP1D8O0jTGUzT+vo/cBMzZzIZl8rK9Li5oBj0U52ky5++iFKYoIHBpV5Ht8jP/////exhyDmvXxbvKLWEgmWGGAwF4UGpV4EBAAAAAxuBkIGtkKBq6wgASMNGny/KgA0JiQaYCBCMICo4GByx0sonArLLCLCzBQJaG/r2y9aqN7L0iETX/HggZI3X4hcA1CWCkS0rjoDmCuSiTAzQg0W8W8hH+o2Lvm5KOam8xKJPFovop5pKBYKtSb1HC5V+xgVUEXdQonItbN0yRQugHQ/Oz269Gf1CN9vYwAI1keutIyrQgAAAAAAcKRoosQtYz4w1VOYiRZDAAGClzkeVKYBQtAQhZk6gKQvnka1VgoGMGISCg5qgVOlU2HJE+WfqzWYM7ErEQRbOlziL+Ph6wnwYJrpGOsrx7RVYW06kQPGGpHy2zyrDzxveFnRQiDAZvfqT+n/U5///+rgzMUpC3+/5/Y1pqp+lCSvoIx1rmGjAAAAojNHgFEW9IRU0FL3ZOXIArFuEwFQPAlYG4KQM6ARlzhyRlSN581TczifbLqhSeSpmmf/loA5oH8/o5/reH4fSMuWf///51VR6kMJRNNzrCU0tuFTY/EM/imT//uZ1vcpcPZw1c5RL7lyOegPRaiuawOHHE8c+aaBAhMAAGBMshAKlU4T9Ozs+5gVtWDphKOuqQHZwz5QAKCZY211MehFiYsIaQdQ38nEXomjD/+7Rk6wAk0kfT03Bl0IqMCq1p4rZPiSFbrL1nwdiwK72Hligj4kExWFTXc4rfNIrLPmt49gtyrLKSa6FdzhBx5xUVJLS90WHE0+Ih3//////61FFGkOxv/1+tujelaoz32CzEDyqyAEAAAAAUCGXhr2kQgUAQWEFlHgRYQKUgYDo0hySYkEgUcLzA0DBliONGrQywwjVteWixuJkN4W8Z0JUeRXL6Q6yz8N7ZiS9KSs0djCahqHvvUMllmS9GlN7//////+fXxtlIP6o/OkzCUW59Hrr31JHL/+5Y6WVsG2o3YoJGwfJxwEUyMahTT4ohWogCCJi7AX+jyAkAAAAAgiF7hY5gh0ZohMUVNdAAIJM9JFB4BGi1S8woBQmoqjQJVNMNrpe1OF0gULX86K6m5GBBCgVMctm+zZ1XIY49JYYTETg9WFlQ05W9ExCcHYeKydxVIYvuL480IUBkEvUs7yXVt5jxpUExUBRI+Zv3//////6KrGJb///516kaVGyka3EiiqP/CoABNq1N8CgQeFTAqoIYo2f5g0MslHRxq6wwgCLQhDsnyJaZFY5no9/7EpX5fhnphwPiDF98RGoWwiBnv8a98/sr431al7////g6Uq7PhaJwKE7Hgr/tblzkt/8JX/+7Pa8+46XfrZjbY8mDsNbUj/qhpEkXah2f17ldSvdyAkAQYle3I5pUtNoy/aNlIF5tLYIs5TR6m7qndNs8Ol/WxLdya/LICibZpZBrSLLvRZczwRbB1pjtTU7/+7Rk7QREnkbTY3hLcIxL6q1p5bZPrSFbrLzNye8wLD2EixjWQiELPSeHzUl9KmjaFxI4/ATnHJLzf///z8igYYhf7GfP6qv//////sUgZyI/f3XqnDsbplLMVLK2YtgAWANVMQQAAAAAAB86TCCCQGA5dBVcFC55QWFA9kSCdX5hYzCVKBOqGjEViptuVcUuGhiAjfX+bWDTlYMNCCjwqVx1gpP+oJlzhr4RSUyjUWfZvI+ziOcm0knYgRuUvfP///+ZCMqzuMY4ZkuJ2mt2t/rdUWpD/+mux//6/S3mZxc7UpkJCaRNTFICgHX2KuMzI1Wk1H6wM8UKzzPDTQYCIAAAAAEjInuNPJXixt9YRbIh8SxX4gAfxXCl5IKmuXkATgQkg0qV62Wr1bOqsmapki2mElqIg3EL1vm4cle6NPlGIo9UfferFdVuww48blUUUylME0MFQ5OSqqg4UEZRhBhH/JEHBU2iHmuXTGdn//////2xjHZHac1mvaxDPcqN399GqX3CikaKcCMQAABADr/ZeZAOHFEe0hkO7/D4NRGNpPPeDjCIKMDiEeH9NBiacTXGGI3J8plffu35IE2i4/8qhyeZLx5s+osWXuNCUVHhHAeX//oMKm//CIvPsZa/yl2VAuaTeSLX//ENEeoSS/h8eXZpoyxw6WHio0WMFWCbChxJhQi4h420+RckPPtbRlsEIQCAAAK+/hSEODV+WzXO50WERawieLbKbMgW+oasM2VL1uj7U9anjDaNrAn/+7Rk7gAEy0bT63hLcIurys9lBeJRFT9d7T0LwgMwLL2UluCECtu6LitpIWk09GEjzQkQuURbvw42iojPItYmSl9T0C0NXUoR+7DldTP23nq5Silk4h0z//////rOSNUUQruzHu3VLutXR2+q6Pq7HGXCnFVDynhAVBAAAAAOrULBArF1wQmjKgy6gHsWoh4ibdd2Mrxai58hie+aoJpTZzqXe7NPOSmq4V8iQyrIIoXFIUiYgOvqLDRqJBrf0MR/zWONf9ckQFjDwse7/6GD681F57bpL4VRNTRo4XsbeeEROh/3b1vdv5X9pMLBFGuZgDQgAAAAUj3UbHRUJehmiclCAZQSk0WQoVX2lV2JL5cJXD7SWkwgh7mJR6OW6eaaA6v5SNs7YcFAMPZROFtT8jkiZGGfqFWS9r6wuO0zdXrHrwxAKhc5tA57v//////1h1MhEpv+6Rm2Z6/ened0rxQ4M4AAAAAJBokYyFockvgwHXmNDx4K+RAyYAJEENASCAQDMENQjqANgq/Jc3SOhzji1YVegOPAM0tiB1WLhl4xAmCnjDNfrP9ajw0kSqy7F2pA7lH37jiLXhhnbPKLn//0z4HFSIVmH//rYZ3//+99pMTQQ9Rd////zzM5ySafFPBAvSAQBMNjokQMTT40ICgnKKCmcE41Vr1a2J7sxa3AAAAACC46iwloQiE8C6Y6HONDLWEQpN0wIcuHHG+H9JxhnhZaXQ159ihCPoPGlwPeMwE40BgMEOCBIQa1ujr/+7Rk5IIDyE/X+ydN0HOr6x9hIrZTkTFNjeEtylQv6nGsHbn7gOea6lczOHmUULS3+lEOX4YuRVWJ3GWqTiTaNPgl1LD6sOiIUB3HRu4yfaxgWKHGk5JztDROeVf//////so3Lmqe3NX955yc48xKb2f3upiPmlXG1XUEAAAAAAAZSl/mXDoRJlV6ap4JSXihrLGBDIBJARFSAGmpDC+Ii+9K6iK6ao8FGi13UTpWWRsMHAEOzr6PP4jxy45AgIBIT6mMT5/4hy4BihdEv5U8bCuPyQx6NkR//1NIV0Rf9Wu3qdVSzUQhR4QsL/PbCFZxVpV7i7FdbqZgwIAAAAAAuKccE670KJOlE5k7uU0UhQMpaXF32f5GpnYQ8oFAxoWhJMkLVAuqiL8mFSP8QgnSsYGQmrCxT0YmFUJdxfPIEONGV1n6sc07LD3CCmQEO5DHN+6lKRH7UUrP//////7nciOz0k+z1Vk1U+qhBQV37FusDbKQd9IAxNKoA14m2YUApYXvYSd/iGH0SzOhBoGZMsIxYUOobCwFyxGDaxPXHYQTjRNlqEVfjVZuccpDQcAs3jcY1+VK8izgP8gYsgbB4ZU36yAnCAB+Y4b/LMwIgYIF7OHtEwnD/9zM9cZ+p1u+v/6hr0dYvU6Lo0RclgnNQsdjcusUH1Tp3ISqkJI1v/Qb6SzP9S3TMMAIAADkmWXCNgIBBQ6JFBEAW4cwaAgK4QgWLDTLDWSDg5K4xAxJA4GQ2QGxGLPIFcqDqWIAlID/+7Rk4wZD9kdVa0pGsH1MCv9h4nwSPU1RjUU4wk0vqr2sFfkkQiAly1cZeDQqlhU6s6GnajsVZYwlpTLH7fV7n1rvNFWXujfd9fz9QxHJValMmft64Vakkut8/95agxRgiZ9W2GEb//////ao9ypIajl9ld0Ijdf0/mu0njFdqpcwQjAAAABOKRF0GyKVA0NslJ0yqk0A5BZrcUIAtk/CyIMwkp1F5zEvCQ3efxE/O3EqIMtymPr/wycl5GSqpvaf/5MxMTj9f+gWmQ5LTb/6+W6h2K/rqFKXdwzmeL/g+jN281npWEEHrsLiWgh9tYgUMvVeSWQVgUlqqEAlIAAAADu/3MBd3oVDG4ChoFyHQNs5SkGWt4giWooaxARgkGVVyYETIiDL5KqFhI9j4PgIGCCoslTlYnlSp6E8SDa9HIkKyc3KKv10FZdZXWTNxM9MzPRgcAAHMCD+INQeGjqf/////1JEgQqDSuyCyTEUSHuQ4kKb5NMR/7MMKfGCYoPWmBBEAAAAA2rYLQtIBEewuKOjqNAW9/kELfZtwlScCMTE7yyLmfZ1uDxS+l/8pTJ7rWX0g80WPzBeAIHhMI7icF79TAfCMIS3yhY2xvy3EZjzEP14+TMNJ0m9H9zS6qR3Z+0iVzGskCYgn7niagZDKSNml6Kc0AP3F/xH+BYAAACymNBBpA8QgFQJiPUR0FqI0F9kf440cKmAcIGCpEWFVaoFNXpWO2dBhnZe53Vg3IMGFkSOzO1ytegpZLRoAZz/+7Rk4AAD0EhXey9a8IZMCw9hhagPbSVd7J03SjUv6rGkl4hLocnqyjcQe7c6/DNXca2tp2V2QB7wN+6L95j4yjDpEXgRt//YYk4Q0M1v/SqdoTogAi/////6/MgscpisZrv/si/P//+z4wUNlIIAAAAACDsZLMIUgQEiuQAlJiHMkercrTxawyDJShMeKoVzSVmoyYhIxbY/8wCMKpjCWKo/sM+P/yRgN5Llea86+is/9kSClVSw4//kHnyxxdf4tXAvS+3U7wpowWnjZmmIn575rPD2ZRRFcWcYKiCOHwkJKDBERqRDO+5Xiepfv3Hup1oCAAAAAbU6wZZeLptPyYYUMhNbVk61zK1QavRbxQAOFA4JLFX7JrDVqZzXtkrIGYNbAuAsKAYi8SC26ofXvHMZufpyZJeNblclFszSFVaqJ99XvFkHQ8bX/0U5O6Y4iER5n9CKLObN/////k/QSqTHde/nZW3GMZKkcr0crrQbNd3cLRRhAgHp2DRCX5QFCoCiaCQYyqHLLLpSj29oCMAQJGBg7Ly/Rop9hwpB6wtRxx8yHQZyXnBngzhSUMMqP/6BJRPAxiShETpNdoLHwtGyyIJF3/8IDUWkBtAIP/UmuUJoMFRourkiILjZFp/3oziH69aSlLMB87FBOCblYuPwHjZk2rVUguhQNzVuzdCjygIKoWJEy2TylvpQrNA5/KGiCHGLBusi6RHteL4AEoQns+UoYjtw5gwQ3ZX+1B3IZe5pTyqiaYw8QR0PQYn/+7Rk6YZkJlLVa09D4ISMCt1lhagRbR9Rrb0PggywKz2WFthtWSjoqXGYg60BYMU6nicI5m8sKgGx/gQx3KRoetXPopvO3GiKgMP/jDHq37////9//6P6v77dSlqrHdDlbM86vZirUBmxCIAAAABIuJVJRtxQbiyWi3Da0BQKCQo8AjCqaRoyIXIYBUkAPhywpiNBihcP9URxbC8krCBEJH1VG1n/anE3hcjXxEbWBUfymy1NzmzT/9KYqbwotT//OLkzSewYv1SkcdCEP/7hXjVV/45Uqs+wvQgC+yMNsKsChJaKtRNE62tm3wz//d9d8vL9LyABAAAABJUfVK10V3tDcJhhw1rOCqBVGm25Ba5N1dAc2MYCMSJhplDSJawcQCQcNY0njAAoURsGQqc6eDft4TwdxNTTYWFXFQbi6IUc0CymOdkYzuAvvWFyRSy1K6OiZENM142R21k1Xy5CIZg5/RDxUjf////+X0KkkjUfyZ183lfZWT6p7AmuMAjo+vAGIAAharxBQeoJKOOrlhE442pm82HHPq/c1MpiZUQDMiYs/qhA9BEPPz57xXEHdmhZhib/3dcncrHsSrnn9MuTFCEi//p/xLe7f/nWxS0IkJMy91xg6CBOen/1NxXf///6UxOTCVqZKf1+oDNJYlOKhPSNCLWxPPfdlt94cQspqlGAA0sgCAZhAi7kAYFFoMm0jIMpdv8gyj80J9C5L1jIIuYrcljPxN214N2HQKpFwpEBQYh+IwafaexEBsr/+7Rk64JkW05Va09LcI0L6q1p4rZQLTdd7L0rwjawKrmmF4k7LCwAxmddtkThoqWatBQSq/g+r6sLY/pz24y+X1MkoiCUKioYpYXemZ2tKMOP9MzCyzrp0et//////0lcrnCzv9aGXR67N+396IhWxIRHtOpoMBAQAAAALamQzOcsuuIV10AwWDDvYa411/NPNgvoYgkZIEanI2WxGhD2xH/aRU8I1hICgLrTULf8q0W8Yaw3rl+4RP+0W0W9h1/2S5LF8vf+0v+INJ7hl2jnP21Z/4n02f//f06esx9AzzhSyXBizIwuIkYkugqgWRvGHVd704EagAAAAJzuzwWIFSKFjQlNHKMNWnFtHvUbgd5nl6qAmElc+8ph7sYcVJhrzYYm0Xh5UCSVA+OzQe16vjs4bGUo9WQvymXhSStVNI71/tZKaPa06ZmZYTQAyr9FlKdv//////oHTs5Tm2Ij0jWSSxGd11XxZvgSZFc80E2BAAAAAAIUGB8wMCEAYEEACJZUhucAUg4ZBQmyuUxFtUxiYFZPJUGmuU119g4OCwYhae1cvgm0MpiFkxMUxIVt/b07wUYXARqNCZWFjx5Esiy4hjIfG//yII4U/4SRApxgdjKQkZNNXmDpKTcuvh//TcmeKotbOUQyxQkNjKH6loNACD4+AhGTPtb4ut/8qwgEQAAAeJCoULFhDUNtYEBCRpidFBIEFQwd+DUMEjVwsuAIogPYhGW9YhIWXMSL8sFL4hYlA1fanknlho2hRhn/+7Rk5YAj9UfW+y8zcHyLCw9hhahR6RlRrb0TCjAwav2XltA7OpWVWjhQkYJruSGysyuaWNkZjKOk4R6GdD3rMUPhMcHgpg91KccU4KLf9TIv//////RkHGbOyOZV0kIjmPOp36m+WztbdZxcxxj1ugKAAAIATCxCZLopzCAozgeLNLOyEUGgKAGfK4MCARHTVc1XprIXajih6VQyHeQIQdt0KWQ/yWLGb/+dWAFgJoJ9CcKp8+/wu1Mc5EsU///sg3/jLHUSFgmEijmakasbRAvl6sL3xH3CDeu8bccDJShRFOFyx42hquK0rDhWcUofIbKn5D6AAAAAAA4qCogOTPKparhQt9hmCvQFFmLl52BoioUw4RB1RmSAu4EATpLsOER8lAuz8fA7QPRCXocYxhKE9Lqn2Ndq9cpUmhfCqg2Y1s5zxYCVFSVCmHQnHEqVxKq1SebaxxIuv/66ZAYEIb/VSt//////7M7yW+rUvsf/29GdH6o+VQxBVVjBAAATDoUEmGANOKpBSgYJ3AlY2BLCJyYvsnmWbIgb5SJ1k68QQ9AEeLr4A7E9LtKCaNNDYv1/8mYP4NsGKjoBwtWv4vMgJwTa//2KXp1w6K8jmxLTnVrmtrIlju0nLVu+Z5jdeq35yeiZyTKcux88oqGahoY0ZR9TXUvjqFDxRPrQqQAGAkL1loB2arlCAMxuETcFBBRtaohAQcQBQHJiMEDYKBzCgQDGaANCpFrKATIEUSjMQMKDCqxSkA1HBDDHqlz/+7Rk6ARkKkfVa09D4IbsGr1p4owQWT9VrT1tgjuiqe28nfiVRICPMRB/ZTjQDQygQWD5qnfyuyx2XLLA6sLElWu1BSsDPm/g13nmdqSRmw/F/D/3O8mEpBG3bV///////ypF5lm+RqM1M9XYpKwVUGF3AoAAAAAsOMKL0tzQagcQExogc0aNB0Eae0eEQIsuIxaaMTkLEIThQOcnigkp9fhImZtlkCs6hkCT3O//zEgBIV5VoPTaYnDN3uBEA8HABhf+JkSNOVjzKFi48cU8SFasXFsTjsXtN+iGHdy0yXLWSWDSTgJJCJ+aY1plseRZLL2jWkt+p9mAAAAAAFpLkgS6QaK1lNsYCPS8tSJMpnzqpwwyG01mpl/gNOkpffWC2TmeklKTNrlbiFCghhNByjrFYM+pPkgdP3EbR6y+FYSZKm4rlKkzxM890GyolkQ9wgpdiwqR/I22IL6b//MDgZFbG////////bR2Me//pSSY9v/9KoUzRNA+sNLoNFB2usMNBxhEhYBsx8aMQJj0oYFQaR6FB3cVA/DzxqxZTaWKkDh/3ElUzKWVF/InG4xS//7mmYJAhjC1YMi9mMuRyg9KAhAUn/8qRfHlVxlVFhCdY199brbep9Fn//2Yc3S3PIcDw6BXlmDw0Lo45nSAWTZsLfY4cqkaCrh7Ld0bAABwhQWEqdtEVRQ9Oq0IA4sPUaaKIBay1gh86XRHNNhcjev8MJRXLyEgUYgsGdDBHhqhrtIDWXMWddsjLJVYge3/+7Rk5wZkMEhVa0c2soSsCqxl5agQKStVrKkaAhkwKnGsHbjAbGUsVvTmMbddY7cF6saSpjqezjuFbh2/B41GgrFAaHopELXYfbCwjqa1Gf///////zrrZf/6b/LPr6LbbQ41T2ImjyrdhgAAAABsTCJhg6wYQ2xJWVwTj1rq8d5qcTaSDDSgt2GawNHXLqM5UjDXefmyt0Wn4t3aw7GEKtf/dMiGAl7vZI5bQQ1DPMVhAg+Cofv/Y8bM7dHcfJzxLGrauKrqbhlbv+bH///vlVVXMZqSR+LUV2UcUOb/SAJC7j0sn/OL80IAMLGwFVi6qAAAAABB7SuHcVRZys1oJ3mbSy/Tdi1KxkuCQ8SgxEXTDJ0DrEsZOHCAywCVLUBCYQN8Bykm0VlLAKiEsdU3TIZ6+8ch6XSh4E0lrzdZ0X7cKmpZc6S937iEMT8qh+XR2EyyKuBKt4ym/936rEUARJ55/jf//////uimGIqen2TVb1qz6153/E/xiRsWowUKzMlsTniAkBFvMIgH9BC1Kq2HaO6n02EQNPn0WxmePzyF3DcVf+WVLvujXhcYiM/8qnQ4cyfN7b6FZwif1dORqJF3//+In//HFkB0ErHCIaaZ3VGGzTc+7f/XKP8DoVWoecLpTCO7HVJy2CKmDESuaeGnDcsn01kAIByOByWSNioXnho54hpyBiICc6ZCOIgHIeCkS+QHWx1VzppYKAiNCruOUXvHSozwxLCULhNfWw3Zz5h14rProbZLd6Wp/Tf/+7Rk64ZkPUtV6ypOkIzripxrBX5PLRld7L0NwhevqvWsHbkceCmuwIw1o75zrGIYs0nQ0DkasMmFjjX9huNyYBg4alvq3//////o5RTXO1ra5tGS7cdRf/19zUayjc7CdQIAAAAAAD8pLNLcCoZB4lCsRMDdUPZMk1Aw6FMuICAgs+bqpjL3QZLKQAERSWFadbzm2NQqWuAps2B6Xke+Kfp2FswwX3QeDhz2PLb7OvLz6zXs3PSohXP/wgAEj7kbQBAGdJo7cTIOP2Mpv2yphLF/JZcViFVJCbDyOU+5I4hEgXFRlVrX3u3nbw9cMVf1FMT6MFAAAAAHhNJ5AO7SWzwgwK7gusIgBah0S6YiCF3REUDCCd4wAAzFaQKVtbQXWitRMFOFgwqJXmh6luxwgERJGtwBMOTxGmylguS2FxHMbd6t5jFM3KQesV44kYTtDVMoeytB0Qoyw1X1/inkILDw6Ucr/Uc3//////adzCjvX+RD0q3f//s+gjhMUGS20EoAIjG6S5cd+URlgC6krJZBY9LwWATEWWxdDgj8qq14w6TtQbauHywa9CfNKvVYuJfm5YQ/X856xB+cnaLjvJWj+mXpAFmn//x9/1FemWm6dGxbzyuhJq6PhGmV//8wU1NxcRcIXN5octf2uSRJZaPzlj0qyelc1OG8Oq0Din5SmcEGATEoDQWkN3YOltD42+puko6y51AFeNwUBLKLDppMneaTsyusFtwJGlitMac5yjjD5c29p9JI1uNtef7/+7Rk74Jkk1DUa0VPII1L6q1p5bYQJT9brL1vQfkwK72VixiHS0EwgCJ5oNdISTwRlRMQI2Gsbi1Q0TLdtez+Vh0HZN1VLWv+W///////RDxifpym1dV739nm+jOVkOYIFFuFbIgAAAAUevktBDQqDiCf76GSgonF22hSYhBhcEDTTxJyUsInr8MPAnCtZyZfhNPO1BlzMUODvv1NvLe/cExl4EXE6RILK4AmZTO7t23pZu/sDPtOd//CzlRHbJHlsD2HCptvcoYPDZOecjf1PMI1gtP9qNuHpghBDu+Gl1QKi5Vp4Og6kP/dAAAAA3xYH1ArtvSvM5JKTsL4kAeYIBCISMFAyQnBxazdxDCYtyDiLRCg0qgutahVYIRGs5VsKfHuBCybLNkOisaS681C2bj0harLUKlclnWc0Wl5ID1tLszSlHjMRn0CK72zUcrlCynBzZNb+UXf1Q0vMKAUScgiYej6N///////rVf1tRr0RNP5/22/QZY66q8AAFQAEEQggOD3WCHLGTZxkDi8SQDc0nwSNFVwkZFRgKMwU1BuTkLbTyVxIn85dT9xd+cEIcvgsyXUOXO4StnzORYS58WiuEBfVmIjMyG/Hmlyb//wVUqIxtTBg3EVaqTI/JsP/KHkf9d87hI31z4acjXZRpE7Xiyq3TazFPGyHGnK4zujnfu4AAYAEIlHZT4YCd+nZeeGWYceaEO0pBgCCGIcYOZQiZ/JgbCwqayMpULQyW2EBJRlzFlF7gqMBBQ4QZf/+7Rk7gZkN0dVY0c3IJFL2nhvBX5Q/R1RjR08iiGXajWsvXhCIkJrFXOd9VcWEbusZwX7XWrlyt8weld77jTDnJWyjLNkmqWUycU5UJc3Cekhv1M17/xP/Ccf5IkLeP/Dv///jnLvqxqEHIY/1bBZ1YlQNgAAAAAOHckkWoAu3MIkIUN6dnoqBCEB7dn0GAIMIwLkchVx1LBKeO12/ykTvPuQthtoG2N/+VuKgW9akf1Uk3iyXVcpxx9f//q5O/m5vLC0oNY+6/No24r2FD///UZKcHm3zBR0jxAFRIg3nhXFA6GB6LRe9DsqEEQZObJ1g3IO8AIAAAAAAXCpAOnaoggjReVZITYsQWZc2rKJkuGQqr7BpKzS2jB0+sEaJS0mVNaUJL+vuSGrpZcmKrcx6Kdp3GyqTxL7VGn2VubUU7mgGkoQrxREDOqiWfv8n7eqZk3S779r+sJgCeMEnHn7ORP//////WXPp/X1Gn5fsrf57inVQ4K5JyAAgGJvJEl5xwQggdAvmckoslB1nFYv0W3b8mYvI6TRoVp6ViLnibMr2WFEl8oUXjJRCW6sch6U/8A6hJifiSFpeAX1ZxbDWQhRjqKfdP/9opfiiBt5IiFmyoevX/tzXykf/9xLOUhJd2LiAH5h4blQdBG+mY6AaVTH3///vHjLzMSeQAtpxQ0wgKqx3FTUiJi4pkFCiQyXbaq0AQ1TdM0xAQEOxtxIAcNmimCEDTU+BocqBl5XZWkrx730hH4XYm6korYBIiD/+7Rk54ZkE0/Xew9D4IUsCs9l5bYQXUFTrT0WghmwKzWXiuBmJhOv02xmaP3p4lmWRWIBla1OwHHlRK6JaBn/O/jT1dNf+VdeN/7bjN/////0f6EK9k1u/uZnlHvn7s/+2tskwRE5EAEAAAAACIdYwPFxEFY20xAdCThA2rpnrD3UxUBBhQokRWwXrpJ2WOiKBXbe+M0X5QUXqtrpVTUNdDO5z//JnaDK/mJubqgjM///yHW41ZZTUX/9E4c4kPDBXEvSrdQ4VjtVCAV794MyxtAlCEThpM40TOB0gmxDKp0b6FBOqmf/+2vKCmbi22BYBAAAEwdkg8rB6H7pO1QFShXYkC3iaz3NXSNW8vYeZmlbn7bkitSJFtxZinqpEuuyhqjKXgjqZvioB4uPkNhAGklg2odOlYhaVhIZLo1mpkgBQlLgnDs2qZU3mkzsy9AVD0kXnas9My3zLf/////+kyVL1TXdtk+/3/3dCILzCnQZ0ABB1KswJBfaOpbmA3mI3bsJdruiQ7QyBC2wcgKBWu+LS25uiBDLJXrIbu8kyGaPoqV2kO6+4/G+fKJZJVKCoRUheuTXG3W7I7fwIo2CYBIiJ++9jMY/oHT502kyNL/5/2Fpi00+j59B1nb/4QNPVaqZJ2bGbnmx4+SSANoZuNzEkDyfJxfEQxe/vXr+V0uTLKAgAAADBIZMA423q+1VEQmsGYnigFIYMPlQEMi0jlgghmYpMOBAEREQBkDTkRWIIXipBJqHVwjQUHG21L7/+7Rk7QYkQ01Ve0JPIIML6t1lgrhSEUFRrWFrwkcwKn2niths5AR9GNRkCMZNH65PiEkoIlRONWIXI0CWn6pl5Bj9XIfpWAUDxXjvYj9FKPFlp3+sa1wockI/Xw+/sy7/////mMUDWGbBl1ZGK25n2X//Xf1BQaqrgBQBAAAAEivEOpEMqYOpa0ZIdMCnGmskclRCy5IXFUxhGgf6xPMoTIQis/6SiNVD+GgeUp3qGUkGO4pDNfNlT7vysdZOUc71b+n/X8c1lFoLas38Po8q3+Ufr/5c+Hcv/TPk7o0WVpTM6iplIiS5H9osHaqLKlgBAAAAAALhUkQXTYgKCSvBoXfOtkNCh67WaO2rckQXTZShEIBKiIoQEhFMOovJj9lZ6AhrzbLvlTqwE+JRkXjgrqSsSiuOeyl8uB6PqKRpX2MSKXMqKlKxQ7tbbM9MhCAh1Tq7Vb/N/////62U+3/7V/faje/Z+tWUO/FLkAQAASDAoSaiBCYYgi5SyMFHfKJBNVYE8iPoVIFbQht3VFWA0133aCBqWBnu3i1tqMFNedaGF+wS1rv1rt12QYG8CH0xN1nPvSDgmGgilAVENfoh+bJpIMtXZ/2jWy/l5+eo/5v935fIz/4y91X3ywGSkcTTCjgkOrXbdKYoBIiH7AgmrrNAAGAE8heo2x57H4Zif6uAkbJVXAgMIgyHMzWABD2blFghEUMHSR4J9Ag06AgVGNDiwKWhj5GMABhXCSCAJC1o0DiBZtsrB1B3aZiiDCH/+7Rk5AJjskfX+y9bQH1MCt9hgrZQwR1TrKzaAkgjabWsifgmYP5xbjQERnYfxiEiYWTAkoLNS5U1HIjEVUG40coguLVdVMb2wMqHiPFLYUf/Nf////85yu4JvyRVY6T7+mXXDIdY+jCAAAAAABxwMKlYMtYlsmGuo20IIcLjY4JCSEGNCgKFPZSUSNzTnWgHr6x5LNypdqZKp52YYcYRg0DFIBVoovq5fGg4DqCqG1gl/leQzO/7rvXF1YE94tz/LGvzoqNiWcf5f8VodfKFTj+rxJ63/NhO/7/87brsVHs/Ej9ricjsRiUtS+mpPE+p8P/2fV9BIAAABBbOmstcfV/y559yQONMsTEFkwBNBygwToAEgxEDSZ4EPJiafqeqwjLxAsiMhGaiMDNXDo8BBeMvgRDVUDguCuhUbNmoSpozDCoCHNzTD4xKH4dtAmjO1ooQoI7RfWMK+WEacyKbuxZ2cJbft156qMFhMAEL0Mag0n/////0+1BIuH/0vqZ7PVqeXAbWokoAYBE9oeHuAQQq5OcGHXYIasDSsBRlnovqDLAK135W0+VRrcff+SIbiqKRrOFsfmD1upGA0IsHxoUKD1+SiMcFkZE/6KPDf5p4kjI86RGv0kZ/1b/RSVn8YOZhFMgeq0LVFW+urNeI4TkQiCYYbEBkUHBCVJf6V4AAGbC0NDZrLLWws+FypNVAMWAu8KOVVQeGkMpBgU8GUJYTDQpSXiVUS1STccVqjonGGJbx7XuLkTZOCOuT5W7/+7Rk7AJkdUdT41hLcI9IunhrBX4PLR1f7CkzwdsSavGsPPhP4v5FEM+EksHedJ+KkmQrxEKpCEQk3JilgKZlkiPoSgaCYKCj/d///yqzP8alSvXteFcTNW5mAEAAAAAACpkGQJs4Lhos3BUKYPIGJgUBLkK1mAGmaGGASEw6AJIBQGclcBu8GIFvEnWCVJgYCBIQ6GpFCajYuZqi4r/6wwEQZkxkBTHEmIg2xaSjz7qXR5nSTLVVP///8iPitQfHtezKcSRZEX3xIN/8tR9Lf/VQ/3//egzvofLqSXJkKEQjQSmFx3EK8YuTjRSnoxnPyIAAAAAAHYCBATDkhVRvO3UD3wMKGgkeYSXuMWDZCeBGWZdI1kL6BA0lR5KNc20J91ClYgs1Bg14AzUzwyqkEYhkShau15KARWVLvU0kTh6iD0ptsmXMxJT0+kcydYCNMtf3IFoTDIBw1EUsJLyrKaXEw2OIly3////////WabR9/3SZeXeqK7VOc2em+juVXQgaPuVnoFLNDMh6yfQOWNMDssMMD3kTZQjRyjY0ARS00x5WwVatuMQmljMHfcbhfsSZYCGITQUf/9fkbbRUD6XsZuZxw/922SW45ar9/+qZ8brMgQF0/b/OvAyeS1Pn3hvtrTS9a9MShXpSlX82Q261s2/x4rUXRbsVtTTQIgABod+RelThIcmUzCsAsMPSff1D2bZussSq2jAhbciGU50+0ICIpBP0LETU6PPBVP12sIJ9ntVlS4M0bv2KIr7/+7Rk8wZEuUbTa1lLcJUr+oxrB25O3UNbrAzcgeIwLD2Hnbi4izmotqvLVF5ziWA1zr6tjxQdGyi5Tx/9n///////eie3rdTKd6vONoQdG6PS7FRzKDg2MKWMgAAAAAA6b4OLumgLT2KBrlnTdLPWAYqxqOjoAGrCJKUH2+L3r0V1LqFasD2ma9oC3T/p9rHJRKBz8wRHM9WHhf1bKKj3Jspi+7DNo25vdcXY9KBN77NFR7XCd9HqLkDok7jTMq+KnW65iO2XNOZB5ITKLTqQYiThR1cggSrPTYSg0qXoLnYwmbFigN6KF7oAgAAAAGhMRCgUAcJLVReQPsbWCGAR4shUiWmaFx4o9YYBKoczQgSkpq2OXNOBhijbSrTEhnBZyGEOSmxdRl8ZcxlqF0kahDr6KqKfSOc7rSVaGqJJe9UCvgqdk0Az7GHsnxuDIDomilSAbH5TFwxVDg/c0g/KfOMtt/////Pc843tTfnMjId3v/rb2c1dGHHFHKACEldR8ifAxxiENQLorkP4d8EwRQFjQFBKxmHoUsZUQZa4LaXHfU3YMv+D/rM1Rtj15dKHVmzhsvkfYvyDWtsBWembHOun25FaP5+HpW30E9lXf4rEP3QWKA7KQrD/wgJiRshHWpnpUcAtE7eKFoxVRHrGHbCUUsSxJbSZc0YuLvDFxPzswgCK6mBLhkFwAKlO62kfAFDzJiIUMOT8RKChbQl/A5JTZvnndFrTKDBDCE+TK6VvIPjTFAg246/FUsH29RD/+7Rk8wZkd0dT40VPIJJL+p1rCm5Q0RtV7JU8ghCvqz2XntGhTqcNNiJ7Tbc9kQbp+cyFIuITBXLtD3xAkNQeKhyP9xQLY8JQ4OW+Ub1qZT////+YYpilqvru2semKZ/un66MhiZQwJgVUQAAAAAABFxKDEgCk01g4OmQpgHw4+qJbT0QWSAxwqMD2PppqJSF/5IzhIZCEFBqa+3BZZCil0J0YYxzRSj6GXyh2sQBGSE7Ejd0SV6qVRDWz8UK7ZZ9f/nULpzenTucOnHsn/yI1DHTc6+kq9/i+Kc0WGwUqhcVEhxhYwzGstBU808CMseNm4trcREuKFRU9ZQfVFwAIAAAAAwTQ8B0JLxHlTtG9mRmK7kl5UAz0KOL4HAhxIAVBqBhY0ZfiiTVGBtcChkX1BmVCQgEk0FR+TCAr0V0iSIqvFbk+obawyjB1mwdt9Zu7zF6BkbN3AYa1ZczluBg8QgAowagNhTDVihJsjCQTjYxFFlydvlb+butv////lFZTF+iSVlcv3Kszq/f/TbQenRhIUMywJIigAAAbVcWpBAU+wUcQFCSP6CmKEsESJTrZS+yCMxaDIA4+j9YO0hpWk3MS3zFS0Lki8/g0uIIlfpL/cwT17///5fxn12hwaBTses9Gf7ZPCPcruZz+1r+b2+fL81pXTLOoeSVBb63z9Ob1DnZCO9PzBCTLfT2QQOQz9g68TveCBFnJmISFMokCHHMACMgor1Ft7HVR0gkEAYAsOwkhUIWp6IjXom7q0L/+7Rk6wBkoVNUa09FMJbL6o1rCm5OWSFj7DDNAdqVqvGcMTgESDZ5AbIpU7cO+OhUERS2OClYHzg9A6OLpoZBOREM0qHwoc86p0zjHWxvZmjp3MnP//6jaoY/kNNX8qkThZV8AgAAAAo8iATgiANdBsKZMKPPdIpQ9S5l5jHpLip4ceXoT6YKvR2qdc6+IHblB8hsPg2dUbDHDdldkpWvf+CYAiTcRZlpKsMB1bTgxqxNBYCMOisi//rG0cI98UmDVI1CNBRxFJ/9VjLXvfdJMf1/X/ai7UyteK1kCojPoSZpCtBNxSNKsdPqpYrTQ6WrtQAAAAAAGMASZehKVc/sCtIOwb4j8i2uQwoRHwVTREwoJF0WuTTRRaMmRACSKxyea83sELwDlJZOtOJWEepadseaxNczJGavmuV3m4zMGTMkf1Y9l8yILX5U3eLOy+sgeyy8a5oFl+6Wx3HV2cvVODuICxR33Mv//////q9B2z/u3euvbyt/0a4wlnMJrOwiRcwEAjRpfZuKmCq5gfRMOeZKz9AUCBgoWNJNPaSvr9TSkVMKaah69pjDtKmLUM4bmyVo74c/be6ehI11FkS+V2oesyahMA0HqGF/4+9+g5msEg8h8p9iM8zU0eLfzbH5frw9LtOS2oIZo3XzV6IUMXMM0uAl4tU276oogEVxc0kBIJvA5enblLiepRtuiPFloqg5ApDgkKXIVK15HyTw1AzTYqsaIpdLAlUdnkpWe7zs2kzZyRO1DM1PHd0LU8L/+7Rk7oZkcEhU4ypOgI2sCpxrBX4PhR9VjJ06wg+wK32WHxCJeB5uIfwOkyqGMbTVuyqCNHO69XeiqPC4drL/7//////9HkjDhrv858qfRB5i5Fyp2PD/ttlRMGHQs0fHXIp5AAAAAAx70BgwJDRRQ5pXr2MztriRCccnbKMAjQQsUsMugW9/lMMKEFq4NbjRPD2JVAFrHi0kbO3W6QMl2H2fy7Vq6WD/W4vybxyGqXglVP//geOlP9Eo8JzRMIqb1/qkUvyp46/r9ta97cXsoaYIZdirMKMWTAcRIgQKFn5rDBQOoJhlr6pcAAAAAAAAZKC7KZtpNUSBMzO8KWWBBSiD3P+IAAwGCAiS6YwYhVYuGoOGLcqKjI0jUEa1CRQKhABMNKYVCs5x5GjQ2drDLJHADB3Se6U1JQ+jyvbD9UZEyxzG9YTEmmPJLIpGWUP8+Mi7L6m8qusnUkEo1TI////////m7Mxw4//VH6Xzl3V9TNEQ8cAkWFatNoPcP0ISi8IEjHJSIFgR0uJqVnPYIkQUuuydS/ElBAg4q36CBJRu2rp/JVB0fl9yyt225SAcsBP3EYVrluQ4yhg9MxyNWJmzX+pKIgEwvQMDn9qDV+dYeEJcsbo32Qf9UPZNubUic7wsPtkQRBInOJtuU5e5Ku7sUio+I58EHpw68sBosJmiAYADBrOX0DlrRwqoJS9CtK11SItpnoAFDUO6WTdn9awrx2Jh9V+qijKTh+6WTSDdGM9RaqZ0UsOrK5JITSj/+7Rk7oZkNkhVYy9D4JSMGp1rB35PtSNXrKjawgCuq72XlqH6GuFtnb1yoDqwQNuSCyyqLErx/G9P6yZ4iIEArDtP9v/////+bNqzXf3o+jEU0st2S1nbqQwdAQER8PJQAEAAAAg73EQ6wWxW2jhDJ4EKDhgRSN9gcDmWAhZE5qkYEhT5RiBENEQlJv5JYG8KgzjlM0FgF+C+Pw6n/YawD/AcxTRbHFaeM64dfpAwyFHAXwZn//cHTEFr5kVLSxSEa+R3/uKR/nY///vLNuMqykEc04fjRYTB0suSNgUJEeDI1sYZNK6CEpr+AAAAAAAWLi+gECnazKs5T0mhNZQrGhYuosHBgk0eNSKbOk615IN+0/diIuOq8ha9h4ZMl+rQQavdgDUaKFE/MNYRfT6OOhVyLuG1mUqFCZhUjusJGQ6difLKKev1bqSDX7vfQwJuBxcu7eiq3//////sd0VyYh/6FEB7o5ZejFO5/LuZW1DltRhAQkPbKipdiAQMFqNnMgSlwkIKOPwISMyAjBR8JUQUU3chckLfRbaRiJo1GvL6FBKUKdtn603+YBTxRqXcv63cOiWVnoy0W498Qp/xcJPxcqwrH2m6//+h2JM9/TVdLp0ZGym+nf/40jd//Dc///9YzO1Nkj9QE5KLcPtCAE8Nz06jhECmECOEIW7xIYeW6N0AlA6OHI1MtUyepgrCBntaiyC3gwEIBgSkFoxkVIouizNWslAjaPzThYhYRAAyRJAUZUgqRRdhysK1W9j/+7Rk8AZkUkpU409FMIjr+s1l5bYR/SdPbeEtwiqwavWWCxg1gTPohQxKWBKlBA9qVXimPSNaNQqLK8YCUSlakyZIYWfuXyd2b5T3ojbphmZmYPUv//////0Q4gNFbBv9bO5qENGZHRbO3vnPnggxAq30hAAAAARQAAJ1pTOxAKWbWztFoZQ5SxecEo+hhMSUQS8UiXotaENLfwWHN5B7+Qcwxk72qNMpS0sxFyp7/+brRalUjFMLbj1p7/gtyms0EGc//5nVgN6kDpBgxnEdvOYoQ53mcUT9kPE4nE49rjCnIpSTHvllkJHoGiE885v+7//2P2gPSxAIAAAAAAcDqI5etx0+JI1p6zP4bVDikgoJDAJAJCSJMWBbdIhItK2FF2IHc9TNiEKJgyqW6zR1MVb1IMHSm605UC0+IkuCCPtcKlFDxfAmCxWAwO8nBMmDi6cFyWHHZ3K4OEAJCYUnlrP6Oj//////9GjiHjUeZ38zpOkzdh842jpp/SUR7zhUpCIcHQgAAAAUzuHSg1QDIN8WrBxFGaYJgiLAJ/I1smYKqu1CVTK25/UiGIBct8CZGjHhpCRICwz5swA9i9492rhSxKHIcV//+Rf8DSqJDsIB6//xd4pQ6x+TJJ3Ff9ize2ajiCf2V0gWHCzSPJMHCo0g4aOK/8df/6DOS8uVBDEAAAACg5iT0JzByT+wwntMGcalgwdBxxVAVNlZVXxFcjYpC1yYYn183haPMyBY6YblYz8NPccLkNnwyiQsPEz/+7Rk5wAEKVBVY0I3IIssCs9lh7YPaUFh7LEOydavq/2UitndxLFyhmWOIcLhdRy0CEHSVphLM/zJlEBiDM3////////R6KZ83r9oMKO17H//yCCeoUmqNgA4AAAAAZogBFtS1ygq+ysCz83U4OHgIGCEZYJvyKAEF2EyZr7XIQ800nOzZMqNJ93ahVIuR3kqzK1UanmeMpd/v3VyNmXW8TwOpx2I1Kqfgf0lwkIMcf/+w2j+HGtORtpD//+g+CfDr3QdfxPHW7Uc+mJmgYEMHhxClzDsm10bvt5wyJ2s3/n7cy/ncpkwPpjYAAAAAAGShIOIF0qqL4bm0U4tEEI6PCgGBFzF/wSArEMJAWHDIYcBjdy8rDzf5YrkhdoVcDDDCQ6ANCyEBnN9gAh05GlevxZjmkwRoMFl92FRiV5wLBj/l0HYcFDd/1sv+01N9rrOYjQNclCIkB5TcqsXfps8gmkglHB1v///////+h3/8w7vY4k6LHOrDRv3WNhjRWEciLYS0DBBAMLijS7lRF9CyqSTGArmVQg4JV1NP10TYTBUMu28utQFadF23W/BpS3ex68gjoQoPkH9WAlBUKFShVNoX8SEBgsKhr/+SpG1/p1ioRw3//ckM16cnA1FNLv+huM3dqgHroWYsQh48a6PJyyQ9M6T/8jl/lyRY4SL1oqTAlQAAAADMPxyZsGqV5nge7MfTQKXS5LhhzmOsxKVL4fRtoeishvOo6rmQHPIEHmdtZKaOpA+ZyJOVGpTYFD/+7Rk9AIEjFDU81ha8JosCnxvB35PnUFZrKUWQd8vrH2EltnXkkyYZD+Zj5D5sN5rMiEN7G9+R840aGCX+jIS3//////78+/ECv1DwiEB84iNV9RU/9lsXdSCUCp8gAAAABBIyGLVhgpYzdCoHW2Zn0puCkDOHJIQhc5ZrfoJn8Uda+TA7EOtNFSDCaTKMiMOQ1egCFiyN5FumWbeTKYFwA9g7S8HerjcZo37EKWL8sRilbv//5NFUf//D/CahlQP6fOv/8Pn0ZyTxo/VqrJUyxLfu33n2qLNcTB1CZAzIq43nJauVP3qHJfy/hS51oiv2qIGkTv66ACAAAAAQBH1DgxvAECwUxxNM4kZWMYSFBUBd8EB5VB1gB1RDELnKnlYAkrQE5i/gkYfIEERvHYGfw8BMlYQkoERUVTGTrpVixZ9VBGGQY/7oOLnMsrfVgyl7+TQs9C5vlZw40tTrdwoDDCUieA2CIUTE2WzNZEKMbyEh+9Z1NBv/////+9b9/7v7FGfs5omey+4wz/pITZB9aTKOJeTBCIAAI1agLOZDfRdsoBT585dTDMYVnzrC0gFfvtB87OQ5KuZsIVoiNF/qot/x/4Sqo/bh94iVCuF6HBPKSZu4gCIhBvb/L+1JKI44GtSf0Zh6adNd6Lq8SMz9k9IZryUzco6gOiGhMQc+a7pgkfc/crP///vIizLDoI7Op4MAIgAAAAKJnyQIqykQLZIw/p0JMmIiWcoZsmTqQJNaQCyFyEV5fE3xlLLL8H/+7Rk8YIEz1BT409dUp2sCn1vDW4PuUNd7CjXAhYuK32WHtHUiJAjDSZWHhCO7RUaisdj+hlE8Hdxs9BFdMuhaduRE4pNRgchTGEAwPA5Fg0LMUe/UVsAce3+z2//////9UZ+2h+n43JMcY6qQOPQiXs8zU80uFRm3IyOazAEIAAAAEipxwsrMUfNNp4UGmJnepG08kHG8Ymu0mCgZ33TxdWHdNxcZHOZov+MT02kesZymLCQKNTijiIACgiOqMd49FcTgvAYGhnU888iW0v4xOGjqn5EapjpoxyJX3Xzwu5P5ImKDaBdlBVLse7ZBOlmiFNxU4EAbcFDEv5h7QDNQAAAAN7vaogciEHVfRXUSN7VJpujxm4FmEJSwbL2UMMgRVaRR1rzqJCrBQc0qXIIXJoYeTAlUuOlJFSXhUnLp3SGYEw1nJ88ckt5EdvQGnOLSYvXx8307M6ODACgfFjT/1Mzv//////mj32o72o66scqIPHs1DqGa7qs8j8fMiXBWUSAAwBK9yQlIRfoOaXMYgchDQQEIGGLxLnkAqYQwKOoGxodHoXYXxCBscU/BMaQ2gEgvjS281VHZgUHRNfJ73nGPI8RD/vibJRf/8gGxpk1/6UNsi+v8Vuxn/pPkxMIZiGMCJw9QPDRCOeeYHH1I46P0dE7i4LHqQXmt3PPCAIiAAAAAPDrrmmCisl2z9OR9DI+LtxdMBlgqFgu4wRAAEGFNfbiiSztrDEE2k2k8VfqxI+oRoiF0TFPaGlaxET/+7Rk4gAEBkdW+ypN0IIL+w9hh7YP9UFh7LENQjyvqv2Xntkgz+LNGoJ6zn5Y8NyKZQHMrakCSrPkgJ5iwoGLA2bpcGBlf7g/GdZLCAQD6np+qf6pr/////Ui1frrR0uOHkXOnIXZHNUb99iaurP4tmqaBIgAAABsWKog5wIgsuQ6qLP8D36AllqZS8lOFawYBYRFi1ew1iII+Wwy0+oWzqtZPVDAJorjHcIP8M61MiyzNEU9zp4GHbvLg/P5zT7rPy2YIAYFhDp64rwKCIXFf/9qGnE8+lIKCjP/8H8eR14g2KjROx1sqR4zD0oRRIge+McWgo8kc+yEC/OOM4deQBAAAAAOBUGjwtXBMDirL19CC2gAUETHkIQKZyQBCgMDl5igKmSWygZbNCQvpLYYHKUL3AQ4LhlePelYX9LzrTddV8Cwp4X15DRw6ShjMkInAJHoliEF7yDQjEx4vL4wrD4rc57vzsUwmGgkjDFv6Ev9XZP////zHfRvfup9TWY7/6fp/5Jd0K21eluYRKb6M0Frblp+HLVMkJPXMvmlwFx0r1eQJOxyJxxrDI17Oe5D954P7Xh100QnXN1vMSG2ECDkhB1selfeYEwgqJv81zStHJuuP4igATHJ//sfyyG2kzu5TkoV//2b/uLVb8WmzDznBLJJ/4eSDZWy3/b7+TTv62Rp5EtnZqAIXw8MAl7kF0AbFAQG+5kxLusrga9AjUgQMvEOLXE+DpJgTMRhCpywBGojGWWNukc7LWmaOO7/+7Rk5wZkalJV609DcIdL+q1ph8QQOUVbrKzWwcYvq72UltASmBECoMRPg/gZd/TYjTPIjgPQOFEZJMSExFgFOLG9qxUHIf/QPf9f/////f//NkRy//JRp9kX2cwy4AAAAEYSIQTRAgAzIwQGFgQ92pCwEqYuUzEAI5WZGAgwYfGHBoYoJ5AJcPysbEczmpiZyBQGJdpAEZuq/kcDQy8g/ANvTCZDGVsCkIENRFVmgQ9Inxbf8lEmkCp3bUClN//7kEMdKg+/5EIfxGwSxFOFVfwdppDnnZfmqtmhA//WoVHDMnj4GQ8ID8aDwSyBPKEdEkE1AlenLl3Vz1//mq0J0C7kpQIAAAAAHCqDCSUubE6qbIwCPdtMkKMSFTXRPEQIWXEqYwQcAFSL0XRMVAZFIhFRNUHaBAQPtBGNzMUQsBN4OoIVqEtUbELFS9UwRfStkEDLNfZL2H3Dl06ovDMATT0K3IPxWG2NLBPW/D6rnnQYeB3bhyJQ/ax//jjA9PBL/Qx37dX///////9R9WQieeN3/6mjQoQOJSphqljnnj5yDzhAAEIIgaBdwdJN+KFWUm44ITrKvX7QGJIGSFJJDTAuejPKZl4VLGJlpWUJpMllk24NKogkU3FGi6pdh92b2qcEkWVhABxFVm/bM6T3VA0BINgvwXQrfiyIVDvQ7FY0sOjW36GvKmauTFG986rCRi8isIQGwQWY1Wsz/I0u1NhKOf/9PlzagpipUAJDTonnIDCRdCcgqGAX2NeQYmz/+7Rk8QZlKE7SQ3hb4qAr+n1rB34Q/TFRjSk6yesrq32nljEZpKUrjNLTSHgJAMHjBhAAkCdKKONADELEcZgFEZ6iFOP8DoSpWJNVtB7s6nQ3pY0j8aWSM5l1IaoWIjC433pzt21bHZU6olZeaNiL//E2Dyk/5n/////V////5zHuQgcf/qYBiFK1CIAAAAJI3CoI12ykYKfYvYvAA/ochUVLOmSeTUISlcKoPUe16lQuCFFZCaOi3LCIEdEFLmsS17Wcd4o+F2hLCf+odInziVlYXSp1/+DwRQpdf/gaHweB842v/7G3w02zu9/6za0skDjE5KEURD4k98WPj4sWONJorePyUlhbGXjaSdUOgKYAAAAADhOFEjKFW+mG9iaUcB9Jc4mCTDWKjKy8dDGlESC3MTkiRL9JivpKlgWXyt10ploNWcovHG5YYFZGVRNOIiKIMB1Zc20XiiB86AlESV52KjqOw8ABgAhjqMHp9hgfOO/1v+lv///////3pmMZbc6NVREjmrKE663lQMAAQAAApuUGIobggFH9poGCjph6OenwxSpLEiRGQsxJt7Y1S63K8oUuuD8e2ZzkqbA7LNrN7nx+5Tv4zxicoqRTdSveqJRAHQbHhf+YaYNU/jojCShO39n/Ybp8wxlcooUSMsxmnCMBkwkbohURL7S6Kdbm341Dzg5bxl99jjAAwMTebJVTTvJ6xU7IFLtZ6w0BKLkggYVgRQWePrSVcOGihKgcFIc050xguJ8FOCwNqCT/+7Rk2wBkH1BWay9DcH3q6t9lhbQP9TNb7J06wfMXqrWsHbizYEyWKNvGbjtx0uS1iBU7rkC/KYm9kERtpklch93qcGIrhxlk4LAuOEjRWFC5xNPFQ8XJN/qPez//5z5ShNqEKnm4o5Z9YeVVlwSAAAAKuk+DnzXjDCUFCVI0g4neVF0QKBfZazQDTjCuAksIa2t2p7EKV2JQmzdsrId1zluko0GlaIq0uj94Y11VRId0Vds1ypn9enfJltGvq5oJe93//5UChA9//wKCJBEOcXv+uTvuvjFI/+qsh4dwXnlSLg8JhGgNDRGdiyBq2NtVrc6K49sdizG5OpbYDAAAAAAEpnQIF1wYSbiFGXWXYfyA0GGEsRynkAwUjhToECCA5vWDMFZLDUNkKMNNcW3PI/wS0VdTqOWGRXHR8rBqKGVY9gpAdVjJAmFZUDE7ClgkDoTTREmnRfDlcpSszMVBUVjwyT/it2/p/////7LSejZh0sPOYaWc59EU802hjOikuUKmoSKBEJb8VV4ACAu+osQLRhYIgQUanzwvEZWTpWdW2FwaggcRLUM6TjIyLhWHtEVBjqiAeuDKIwA6BZqLSI/gOb9gL+XcmdUhZyq5seHgKBAD0wLf/pB9Of/+zCKXRtt81lzzdfu7zX/6fdCUYtu5DzA4Q7gZXNpTUWXd6/cUYo0eK8jLvemADAAV6vW0D9FuUunLVRdI6xizBRYUXbpKC4bL0z0t2krl63jza4TgcA9RRFyQxWEULuTpDlv/+7Rk6YZEck1UY1hDcI/Lqs9lh7ZPuTVVrT0PQfMv6/2Hijh9FupH0lqquRshWdPlaxxlckIUR+yWk1PzvJhFiskzJj//KLeq57Gjf///W/+//////z9y7pzEihmQylpl9yPN8M1pn4ZleiAAAAAAACgXx0AIw6NghBpyEAFAQew+j6pNbcGr7dUsDw5CEp008FjuDGXw14hG0bhDrk3FGAhiWJZOc9u3TnrOElT5NGNBPGjaueSObxjUJbsa//Pp0Dsf//JojhIHgzJ8ZWKf3X7pGP//rcQoBx6kskeJ0VxQzLlhexgo41HgR/x3BYe1jvioif4T3M9PmdQAAAAAADSsvsmFaw13TyZnR0qBH1IGC3AQuipsmhyAQYiJOGkDIgFgzVIhqYk6HHFsEdhUFNogMQBMQRJTBvBMocMpundCdl+ISgUUwmu7LieRokgP1RYFtaybN+UXRxL691HVLrev/FFBDjm/jG/72////9KT1KV9FoHhew2eu/8gReX7WOgozwc8GDGQCAAABtTCIQaAUAQxcyAhwA4QmGM6Ay6UjdRBFBGOpVtdhjzi7dDbyP0l/XjvezcPvou2MsiZbJAV+0uRAlAnTOOYeNjZKUh5eYq//t+F//9NZBRV1Jf+Sn8N/lM82a+P+YWz6K7U7Hw6bVJfW59VcJ2enZ+2+8wrX13jFBN8S/+x4gDF4zqNpaIwrBrBqjxKv2Uyti1Ikc8SUzOm+SpWCchk8QVXkz4rYTldZTBhj0NBTlS5T4f/+7Rk6wBkiFXVe09DcIsrmq1l5bZQlTtb7WFnweQuq72GHtE9DU09lIcxFUsjk02z5yVRoMT4rP1alxe+4SBQsea9/mDpUkKQl/ypart//////3Vs370GjqcqOm7P6kyR7/osyS9HdVkAAAAAAGQohyBQeVBAwchcEuOXsO0MlSBgYoqwsYAUjRCLjoIjyswkVxv6JOuwAY0FwhcgJMRDgRkqT6N7Ryzf9unEEKtYMtCEAturfKVaDQJE2//9bekopn//JQHB0fRJsoc/SiYRvr76OyTS//3P/fWwvb7ig6RIQm+ZhC8Z/5q1Utl/83xQqRAe5A235XsEAAAAAIt9WUowY2WZp2Up3mH4W9R+ThehEJH4YWS6BxAQMjynLGWGF1oyCgl8NZT6QTMgLooyERbHWsNyjMIjSyHdZpE4pAVQBVpY0vBeJAABgUhEKFCGC49ljjk/8KkaJawrfmZxjgGGFI/6mISn//////MVHdjefQylVRrEJXZNRweMQlb0AAqFE3aQXkYSSUsbBQ5eiibxpNtwO+vqkIMHAoYa8XdQ7g4tB+4JqzElVvZs7LZoz/zb+z613Adx/ed5//SYUrJ4lDkdpZZAHCqDhALyhD+rscV5+CotB839KiYvPfPYm7Nn8xB4koomVbE0yZAyjGQe2z8sc7rQv/vW/1rJB0Ji3JfwEtp54QECikJALyduEHVfEUWE+1B2VkoxA4JAlZSxEEy2k2KQaIYagaxRmavndGB0PVYUdh4F3Ykii+P/+7Rk7AZkf0xUa29L0o/r6r1lhcQPfTlXrRzawfWvqzWXntAQ10Z6qtnYC4RHeT9IyomZnYJNUXbTM6sOkCYlsQMViXQcEUZB2Z/2JG2f//////qyL+v69fy/ql9tzzajhysKjVkCAAAAAAAerOJDZigEYSBQUIggSFznoxEgwECR9cARBojHE2T3HBT1POWIzAJfEBGAUxUcPf3U+kTVAxKy2nSCT9/WEixiQcI01tWdXHTjUUdVTh6Jlr7X5Q+XP+u3LD49WvzbwkHDnv/+HhOGvzB8jZL9Pz9h8hGoiVIeqeHpAjjA8Vk/4QwSgtKIwOfeziVYMCMAAAAALifWQUAg0ZBiLr4TLPnBXgkGNIihaRym5AMRaAE9yCgYsk5q+UD1dMgEIQGbQAtBVVDKDFCwL+TdRFsWmYnZBNCRVRBJWBURefiEmocZ/nMnVGoEisrLBBhrT8uTjChWkf/yRBeNhICwt/yJq5z//////83//nqe/X/lRaNh9vHyREKsTlR8klIgAAWGQg4MCgQFDBUiKk0yjZ3VEWIsmd9lyIwUFADZM0IRDIywB8hHCmUV/r2IEyAtA31ASzO9OdT5oEsO4VDLBqrVQ8QqEnG+GdtHv/ZFaEUv//nJ86xa////399Gv21zn+a+/vDG5RJlfFsTCIC07YWm/2VoG8dq7+HWG7eWABAABAfQ5JFl4Fiu6wKJnMGwWPsHeVljSWDF8ED1am9fyALxdZ2keW5kwYIEglWySSBgC5XmlqXh4JT/+7Rk7YZEiEZT63lDcI9L2r9l56gPyRdVzTzNydcv672WCtiC6mRFIOqL5oZGZuBk1TFMp1r1Oc0+PXVlp7f+c4rDDf//////////+pHVen/UDUrdQTQQKJHFhxnVVIIAAAAINHSIQSTMBDkpSyhABmWUi9ltiwq+hKEhAoQEAJMBIoOrLZM/MuQqfQiHVu0m/ujgAiKJCXTC1pK8wkkExF02jMNTCSJbu/9V1Y3D8OuWr+hcuO1a3f8wMiGJY9LVJz9hu8eBECgu4Z/7Hpq+zfSNffcs9aSVla507wsuaotJSo6FySv3oOpj5W7qxDFSf1JKAIgAAAAAOF2IkGTfR7eVZ7WTrjGVooocho2zJQslKpWmYOINJKCgF/neDgLSk4Uw1EFcPwpehzeYMLKGRtmyeOWKSJSHLMsjnBmFMeXwij9SsQgI6ieiTp+NDVkRHplDi6Hi50iRae1Mac9QVf//ev3///+rdpdChAS9X9Hcupc1lTT6jQ1TezGIYOKUONIyCLEKBAWZ3cASVPFF9j5dFpBgpKGaQjftgUUZM5wixrkWdRQrdSiNQvURfdf8oidikixLyQQn2+m1dCfCej4VrI5xZ30O885mOZB6/+GHtKONHfPFmlBS/f/41mYPqmselrp3CCskzjSeYJzihtOWsD28bnLSGxTxUKiZ0zriVAAAU6N7jriTmgOBYJCRFWq2N4sVrLkodWBoAEvS4JYEdp61OWfPgjaja5Lk0bUIsXSZS8kyaGy05WrfNcH/+7Rk8QZkpUhT43hbcJLL6q9p6rZPfSFZ7T0Nwegua72WFtnEMbqTsyFJYBRaBgmrD8OLIdHIUIpLZyGjmzs3tEBRv///////q3eZ1v1TT7OpPqfqLoi+wqJiRgR+SdVpUBEQAAAACSsESwewaM4wCogNRqVm30RDqxN5xFJFFSJ4NiFNpDGKx+n2BbZ3rR90sOYtpkoRzLc/+12cypDTmaZFFTM7SMTHOv/3vtBU0f8/wKy9z5U/2fNuhvqu4l23duR6fVH9G0TkD0SjziYg+nS50GySi63/Xv+m51SqWiTvmhABAAAAAAgZhjUx1jIJBScqj7CwemuZS1LhV7WZcX/QHqmiqFwsum+lQrDcPkwQMpN0cCTDrLiE6CubXFkJsgoClWUijDuOcn2upVQT85Lx1cIAqCvTyMgSYq4vX954j6v+L4OGwkC0uW////////+yTETzf3dWVL3RPdDa+c7SgbLoa5NTAAAABpKALHLVpQxZWkwoHOQgQqACAUDCdEAMFQgDMBH3kDBA4sti1NQgvuAqxAgfED3R1T218JbQluClD7PcvkLAOvB3cJTHS95CSTJwEpqutkj2OLOaqOnJGhu3Mf//h8qLmMBs1/R/PyIE8Huz//P/Zsy/vranF3+Z6vNXRS1XtD5RIwiIxyUyBHC/JzDlY56/jDF/ebMuSjEK1AIpmelQhgpcJlK73UNlnGDrIasRJjLcIgoVobDRE5m4q6T0Qha2IzIcUmVfF71QipGDoTm5Logy7Qz/+7Rk8AJkEFDWey9bYIaL+s9l54wThTFNTeUtwh+vavWBI9lF347eobzRW6q9s9rQ/DdEwGR0jgxdtoJhdPPy2pKKaG4fopily/uWeUULj///p/////93c3+5ht7AhYEc6kq3erCyf+lwXYPCiEiopY0AAAAIxIDERZduzXwUHl1Do0YwkGKAUtIKhRiIEWAMeB0rgEKhEu6BKkGh4qHYKkN5Ze2gpm1T4biQsiAN62uBDJb1fnJ+lf8EHmAKgs3KROFK4EcGTfpwI+xZn7Zv//KQ1RMhsHXdeSfklj+W//88IovrZmmsoy+6rhytFbU5XebnSUIA6Qo6V0kiYbSzg3IA7df/NwdixrKPkCSAAAAD1Mm6PZlbKsVVXCAMw4xddSZd1MFBpL5AWOCb5uK53/lQ86lLYkVSID+lnCQRbkuexUGiiU7AUVIhDIOTlDPQ3O4cBXoo9ESuToq1QFrdNS0ZCLY/bWvq1pDMIh8f//9Pf////+Yj6epkGiryTsOo8qrVuIl/oQTDoWRR3sEyY+YtLAoYEhTCjzCgUsD5E1QoYpUsCbuna/FI8jIbPOwYke14unUoKJ43xVUYhcIgAGCF+1VFh5p+ePjQO+ienM97zS6Zd/LZ3kdYfRyO07X+wbbg4af7r06AlXM//0VEVzhys/bj8TdS6mfNeQ2ri0wjZkYJHDDCt3vphGHErPVKOdu507p9JtisZHtgAgAABgzocCtAWAAQRVMulGBMmdV+FQPLHlMmVw0vCKvNDcP/+7Rk54Yk1ExTI3lbcIGrqs1h5ahRvUFTjS06yfEvq72GHtFoqSBOlGuUQ5C49Fp+Vr5TfakEQ+iYbmR6SXl6MntTWvuq169eYok1Oj4cHGEQXuNShf5VjhAJv/H3///////U56MzLWhyPOqcr3T1u6FVXyk9YiF1xpFVfIBEEQAAABWr1VQvELEmh6XNEgI8LfrzTTUMayO02SFFtlhTRMZNJ+OZ1DmgvISg0eQRpQKwpp42tbcywH4yRvlUa70ivbD//gu6t//8OA8AoWD9b/8gcaOl3uMZMw0+v8ETDMZOIJ5www9xy2vfGQmgqnFzxSf/j3v7lT0AAAAAAEAaJKBr1W0yrKPiBLtNq0NlTxR6JMUa2x+EOU59VurkI1tusdvYGZolsy5oTpFgURHJu5otAyKVaGtBupmBD5WfvL+IqmiJer6ySoJB1nWK1/6LBU5///////CJ3IByFhEZMNFAABqwYcCqzCQoYCAJQBw2dsSCQgKBJgAarkCCI0jhhoQMTMvM4zO4IDqJkCCqZDKWrUCWy8VUXCAXRD8ObQl/HYZ3elSby7hZYNQESkMxGZG93S+ZPIWUjKOVmP//ZlhFkm05f/532JC1tdMjN//8VxqSS+J/juETdrblt/+wyQ53tdMS+zrMrAr3rPq8f3cl1VUsnasq+NG196hxPXeqPtpFxuLK8YBMLuQRp4W4XU0EtwqZVZvLbxLrYM04IKMAdJaLDlwOmRPthkRAgItL2ur/d5EuRJtvg+WQ0aH/+7Rk4gJj30/X+y9C8GkFCu1hi7QU5T9NLeHrwiOv6vWHnxBNtYcF2ZIYS4EmQHV5+KRUKV6J4Z5sxj4YypS6cQk0yfF8UzFMz68l98oTEUMqODf//7/////9Dkah5z/56SuYZOz2oXIuxd2zjlQTOiDWo+q6AkAAAABMSkBZhCEoTTEQgUNHT9ZecuW3JyivF3JumFySJvUqiXQqw1IFJTqBo23MKeDaFIirDCGTqN8qtCkBKNNWIfBTThz9nS4lDNb//SSMl17/rsrIQQSUFrP/eoxA4fML1R3kpanLbL/mfcxr7Pliya5rdFDoruVR3rGnDJr6bfJm6E1p7UtDAAiAAAAAYE+wg4EmW1mPaoQFTmiozcTp0HqrVyHOfx3NrCTVsFvU5XMqvWj8WGANyuYnIID4TNheROmd0UpaG9YKmK1nWFityEw5gYTaNb8acPigdf////////3T1/0TVzo3s/ke/rEmGjqpbCCAACSFzBADpARpCDF6h5jyRCDP5QIio8QSRTTL0oEkJwCAJloQl/0849ByUw6DB0h5ZqzXhiTQzAYBNQxEpKGA4Xjy611ea0i+ZYAMtWK5aGMRtrm7hQF8JX9aJPKx2DFU1SZxyaURak5zU2+YIGp8ywnDxMCo4Uq///WXVs6MvKow0m0LjQaBVV3fCoIgLYb///9WWUzIT76UgAwAABgPHKoD8+7LZHFnkBxkfxwCt4kCoq5Btwg5DXkjFcNNXwvN2waacR7RhcVlQhzaNAKgrzn/+7Rk5YIkTU1V6y9a8G2raw89haZTUS9NrTU6gguuav2HnqDbStPVTmI07OlwiGoac+kOTB+J0/CoVDKU7EcRdSasWOejLDX2at///E5MRhSPKe/0b//////+rZ/+Y0i25s0//Sn8fDZMKFDEdehAAAARnImh1SHMEDCgYKjjy+UMVuBgZizEdo8iglJEQ2kpxQUyQOaLYRRkGf4swTpdR+REMjGpc3NDOLf+lswKZhjwWBMsUeex9ILkf7bHRvAm863///9AIAPVK/deqRTY5CaN/+lDafUW4uYnxf/e2sd471ipznoB2CKVG281e267N7Nffy5KSB9jNeAAAAABrrXbXa3DztO0BvaEMMQkMQVkTwUxa2DjSEEgONwNmawpE8iuUJl0kSzNIekQdFyguQxAFDplNoihCQvArT/JMnxeNInppF2nV6aLIWhWgdgjxNFyMcboso00C+SWSBoYj2JZXlr6/9VAVixR/2///////ryX+7to8yIr/q+lPIcJDwgAaaC+7CRAAbUCgBoAoahQZDmpZTmVc6qzWDtxDOKgk58Bxk4UygxIH8owIChn9B3mWoXN8RoZsqEuv8QVQK8VBltqqUkk0/1ANgDAxf/6ULGpdf+gEhYNdNf+8DTjK+1QRhW9OnfmBk7w1PYwSFjROhYgm3FXJgCx1Ewf+3BRsT+xdlpdAJDAAAAAoC+4BBNeW06kixV+nYgxBCByGMMKNxdko8NPd1m3ruTSr5WK15lsWW+2TCM21+VWANL/+7Rk6QIEZ0ZTQ1hbcovL6oll5bYQBUFZrL0LyeWu6/2EntmoVVD5KQgAGluV1sMlwqofSgs2KxKgSLnlmjqC5Z//Rgfu87+yf//////qz9/sYfa+Xnd+pkrNt1HSJo8FBfzIKnCEAAAACGGBDgI2hyHRRYCNYZQZnqnAmqRC2sLpRuDgggAAgGxd8XF7KHGWUgaja+eNZ1VtJUoZoA0dZNlZpf/b/tJS0MGXRRZXLYpDtS1k4LmFtBaAk5l+ZF0+XhvMl/Hwkw6km6kn80zCq54fEXvmX/1dPQe5s5uHwdwpHH2kpTzRzFDpXE2g7ZLKamk6Pik2NS+GAAAAAAADNvgCo0QBgMnX7jsTCArqUEjqtaNaZa10wyqhWdV7UHKiTtx1Lh1FL1dwwQNDyp0YjF01qdGle5qpRyrSIHWW1WuDfZIsjMxMiihxXA8kNm3DVy2x6vttpr//B6LIEBpOjTDN//4MVzb//////Sp55xm3ehd5bos19DOVMMU030YdJhQHZQbMOl1pkCAguDDQcsKjAp8HGoB2sjmUYYczSVO8gFQEoUmmbqVbajhD+aXKNmQQQfaTElAJBqJOr/X+ZlEQNVmMj3rZN//K+RC02Ov/5hMOi49/hTCw9/6UFxEm6kVsinspiD0UUIlVKBxMCsRRxWshxYzsHPR0IjIKhZU3K7YlgIxAACJzhfQHGvA2bRsRNdxYZMdgbvpyS5qjBIJlS710JVPjDMnry1c7aNIh1qCPz9viiy6MTKCUNPL/+7Rk7YYkm1DUY01eoJEr6t9h56pPSTVXrLytweiu6/2EntgFwH0NCw6eMq4cQfACpMpLkwLksm3CppFOUmP/+PiosE54r/8t+f/////232d/6qp11PX5P0RX+xA9zkjsI7CAAAAAAAREIx46BHQAqDHgZMLRcJJ6FJEEcNjMWLPJENCjKlrF2uz0wkWmksLLqLvtSXJCWnhcWt1lUfba1+GCyGpgOACMUYh49jjR9EbBmRAMAlX9RTLSy6l+Xi4Rcuv+tmmhunnT5Nr/orMj6P18PI4uXJULhg81lLzyEUTj6MB1vlTj1WH+Mmu+SQ8KpzljBAAAAAABVIDAYUagVy5WhkbqlzBIgQlNAOAIIhUDgNZkhPU2iA0lgTYJfAGwHMEipqpDjHA4AICMONcGzs1gSG1ZHJbhKi/qlyOKKqoXDxtyZmbdeRxU0VdLBdzPoV2AX0oXefmJy6xHMe2//yCZQsGV/+M/K//////GkPiwo/zI6uW6IV97c3QQpEf/CyErRpLqS1qCICAAAMatZyX0UvKo1MUMooBcNonEvyGTPDNUo8hPFLKjHChwHcDShQ/LEJKd5IylQ5KP4mveIijsjp+VyUzSqIf0HRUWDR/1EsdJf6g4DwyKRiJHlRrcIDjfIvP9UXRFskVECoYG5GYo3PKGliA45hh9mrejdx4izDRggHNEuJCiIvEIhe7Eb09L5agtChQKOCULsOAwp2WtoOPLDd2NqD2lK2TQy50NUqJ73uYulyMnaDo0QOD/+7Rk7wBkh1BU61BOQJVMCp1gqPYP8UNbrDzrwcmvq/2ElthAZA0mrF1QOCUC2MFAabeSZbGjbgYhcI3v/5iCIDOn6vp+n/////6ZSf/kfKYup85h7v/JVg+Hx+IJeUEyMDAAAH5N3/JiCo0RU30zXSADXyTrdeLMJXO3aTz0jyl85fltLCdz3/g61LFNuzaB6+VYfG5YSCdRSeO88mSExMz6iJVf5gyLQdERQYL26jjjpNvQpp9ej0URxpSARYOcSCCjqCVXWlvGKMnf8+sY7ZJEbqj95gAgAAAANhdVUv9K3eqvtODZA0IDR0KlWIdE1Cyyig8aJKrtisFQgEgVy/4WALzLAFkUEZgGJHmEmXWBIMPSpw1CXoghgfyAO0sJrxDsURVCfJAghezQFjKAhbcVz5rW4rOgg04faneYkv+ZMaidG/GqZVv//////fShj/Q4zo5iFDtdLDYsh1Dew+YAIOgJCLOFYXYACAAAAAmFi+hMclS/sBBiCcR74MfGnVYFU2ZoAl2qDIlQlxW4ya0zNpzYJmQbwaIgNZUVCFZxppJqzr/mb0ApWqBFgJndWgljoS3uIUTwpQMBdAdb49VyT8oo3AX5F77rao0n//yh77cQ+d1fftxbMY9jTEQFpYUYvP+3xjSfb//saNzFRjI/a8AAEiVrIuVBxOanYwyM8naEYxBEi39BAooZRYviVDNOTxb9piOKh7BGUMiXqzZVQwjZI0kDbEiPwiB6BwmM2KY4lKUQsA8mhiVJhnD/+7Rk8QBjwUxY+wc10pRL6q1l57ZRKTFVrKjaQhevqv2Hitk/S6HmSrUC/ICcaHqthXl9nZIMe2Luvu9wMLBON+/Dv//////9udGb6D0bf6OTgwB+boU7iSHaHAGlWBAAAAAAAACDBVIYsEkaIAYoATOew/VtUBVEiMC8AFFmOYLaL/MMdKthOUqBQ0Fb1A53VRJQPo0gk4u4dGFbSmatY0jRE7MFMiBrkv9c7ajwVyfELNZY3/8FUCkP6r/LHcCNJ/caN9Kaf+4sPFTnGDMz/HdjQ/4OKmxODYBUYDYB4sWK5HxrQk616ni4LHJLY2Wdk4UAAAAAAAAIJ5o4nR7HDlcleU9WFUJqtmRaegChVa4ahadrOGDOvBiF76KKLGUmnKvogM47SEZBUIsEeCzEKNwfxuI1XIk60OTjRlVNh0BEmWqENOhMuBnnedrReMu5FapHlYFqelsxtB2Qar0+Uf//////zL1NP/vQ41TzB4ZzSj23R/6HFXNMdo6hVIIAIBIPX0HM4aTcCwcwQoUAH3VNOTgVudpGgoBqvXoxtKx9Ig2aIK2hUImOcmvkox5hthGQiwl5YbaPff706xXlaPWvKsxztS7DHhHGhpAVQdyU//4xRHGgvHf5NCQgKCxx9zlnbnpZ39DTyRrDISf4vlIoaSmMD21EcQoBgjdrGwWdRTf/38NIycy36jv/Jt/gCKtTtUEuU5w/gMJM9uYMEWCwaAXri0uTVTJdNTtS9Y7osloX0kiVqFM3BL5MhVz/+7Rk8QJkoFBT+09EwIwL2r9h57ZSKVlRrT0TAgkvq72WHtEupEN9oMpTInQqC8vL7TBdTGkJTPlxOJkQRl9Weit8qn7wrFIliWQo9u+YFiZQXlS8pxO7P//////7z0nP/0LHGOOFT5rIdoVnv/Sa7IM1PHG1aFCTIAAAgBW8HpQOQEP0yImTKA9qFyW8MwKmk0dlAtB806jlxDjaRVcnmvBwthebt+58zCelkTsWTCw0aXkB0Ug9f/Tu5T/+Q7Gh6FjA9UPMxcTisnV/ELvUQ1/zf2SZGsSeIZ55BZNvE2Mko9hHGxztSxtSMijB6lxIgIgAgAABgU4iFi7TFJXQyACKXeuh2WavDHEv482FGpxnKhuSUtFEmRxpkslbi2kUSpZWw+Wr1z9YFo53L55ZmjbqkQwPRHB0mqtefNtHDROChUug2Ob5pIICovOl5R9HP//////+01Z30q2y73NZDvLI/U/6E1Hy/Wa+AAAAAQARhYOnsxscAREBigoD1coGCEkRPiosLGTBoIHhJYFAVwU1S9jeqdjCEvxGJV7NWn0zVHVCzSLwasCaHzyWimsvzIAM8TEB0H1lr/NyUBmodtcfRr8YgxSyOf/+CX3aJPr89WUh7PGB1ZrYc732Uz/Kpu5OZt7fkgub6OsUsmAnGwYEEXklJRi72Oo0HZAk6Vqh+iIgAAAAAAADinEpBGGJqlUEDIuEK9WoPORoTVRNZ0Y9pXOEAhQYpuhe/CgzNHCZ4pdEIsqRORfZaxZRcFj/+7Rk5QADzVBYewxDYHvrqv9hh7RS+RlNDeFvgj+vqz2GFxE1JDqsS269mzAwpCEGQ/WTjUuFIxQSoLiQoGTpkfR82WTFz8S/MzMiYEMBQYpUHUeMNZ///////dxo9RX92p4whUqU6j6lEyibqMO/yiAQBzSDk6qRAAAAAAAoPrDl4KdSx+1HGvHslHVmQ9EFrvsmCKSY7PLNapJUgJILkgDWyznKYY3RNBZCxac2/7yrlsG8Tx6teE0Nb7eG2egtsZn/+Q5LjvG0FGBBF2/TZ7Y0ICxHIdk6OeRDDlccRUFxomJDL9EEGV6ap28VkDiP+lpEAEAAAAAEAnUVDlqNt2rw+z8cM1FdifCd6vG5o7t/LWRMkhtuMPtRj7Al1yJ+aijzFl2JcrpdfZqelIXI6QRho4T4vZeLxySViQyQvWB67E4YKw0C0jnP8qUHJBcl52d///////Of9da+Pq3t9qVHb+6ERw9gM6sgAwFEyRYaRACzBAVMUFUEOWxVOEEl3KTYQZQgYxWyt/3AmH8vcHhcOzLJoFb6up2hc4qwr6oLU+bY4a+WT7+teSgh154vuP1oVPzhkxKAnw/Du/KyeVUvOxgcMAOPLX/8+jY5r6D0wYh03185qQLkUr04cCANOHCMQOj8uBHT9fh+CP/FmWZR/0NRgAKAROQO+LNvo0xsq8DO7TdQAt4NFIOmiyDFA0MHNnaeGHpFoHSlZMYImCsBSlkgOGCo5iOII12JRopLSVibZcKPkl6pWuwxT+T/+7Rk5AZj0k9Way8rcHgrqv9hh7RRST1TrTUaQhwv6n2XnxDhWMN8vzlDMaFbImjDMogYWt0YjIZaJNFRqtXSuP//U04EBQXzf6t/////0/One/9/Muc3/b/6BH2PGy04MCAAAAAADZnQYVpRgFDCz7pQQbEy+RQBdrouO+oiNTXXarD1w5fE1NIUqZyQbl2WOUCLJYHOhT5IsvUzlKzD7QweLujLFbp/dFw3MuydOPX/yaIK1/84wOzUZP/+pGGvNeJBQYWKKo+VtDptpzCeIkXHozBkOB3NdyPM5kWuq2Xv/EWBiksIf+WayAhAAAAAA0HQuG2d2RIC+0qVGbEPABgSDpdKDUlRCsgchwQkPo1iGFqJNukytIVkGkVwQG5bjK6MIGAlhDFXReVlqjn6cK7VSfSsL2Tp0rLIKWfbOhZpEJRipVTjoo1Oo4+Zr7/9zAomHhc092+31//////VV/rMZ+iijDzjlF29P/vILrVwurwAQJNBi1kym4OOhUgIDRgf4kKMKZFQCWhf00A81x0iVAZGPQ4DR6RcUMAR2BhCDb9Xs++jPmbMrdplQcpYNCXDlGcQe5n0tSxDKwkMZIvd7VV5PrjY1N2BpIPA1mCsf+ygkaa39JGwgxz+5ckZj5/okXGBTxiT62tjH4NFij6WA4HRlgnLzEt/NxkJB5KK8L6meW1//VoVO9hJu0ACSxEig45KlMaWPBR/HpamEeWXBAS0C1wV0C5xjHFHvS54oeDQR5NQxJFOoMBSTBT/+7Rk8AZkUlFV+y9EwIkL6r9l5bZTaUdLDSk8SjgvqnGXi1E5gAAgRxllBYJAK/KaLWGh2p6XQTalAXCch/bNRwm6srJYXVmVYdmjSG2qK2s+HKOIY0+/qu9fbueC+Vr55X2//xqb966/////VCGOjd7fkcUAUUopG//7Ij6KCkU4EEAAIAAAEhoaIUBuQGFs/QQ1AbMPAFQ2DGkScFBqHJnl9IU8jAHRjo8stJKNmvz2P8nOk+ihCTWUqFV8m3hvrQ2kJTkOZxja0S03JCia1f+s2v//8RwcE1v/+TUkDNOK9VEdyyMH0GK+gcTru7rk5wrL2MQbLIk8NE8nZa61mzGfng0Nh2q8HNLAYAAiAACvW95A1WxoLipg1yZyjjdHHfL2oO0qBCKWfE1zO0RAjjvS+tSKCLGlDQJqy287ROJTavXrUqPiEmv8ngQaMkpOekTE7T1PZKWY8FOnf/2Nhg43OvW/+dX+9/////9WOOghtDP1O1A4IWVsdRNfU7foFQh6Q8v7DIAAAAUSQT7B4w4UCjlKE94GMaV/CysPLCtPXAOAM3V3E6aHZhwRIRlq/kp+1ksSbajH5ACvbVD/e6eOFhJRPFmdHdN9Qkmw2EEKh9/5JZmst/ve/jF4nEYmJ3/5onRKiL+Mxp9RDZrntRQ6jLSs4bmI3lRx1qPmvdByJRWlB8tSDGz2AkAAAABAuodEkXSeV4JJGyMFqrwMSSocRTKPDQIIBU0R5TGhMQLjukoqGQKUd6sDHLHMHQL/+7Rk34AER0/Wey9csnwL6w9hIsZQhR9ZrL1ywfqvq3WXnmHgSWMW54sqA95k4ozdfoJLwIKlWyWsTcwsSocyZrVY0hwuFIRmmOaYzvqeoZLmf5qP/////+n73det9WtQ5UV5lP9/5rqX3H06wQAAAABAgSCr8uHRCN4OLsPN/KQzBgBIRg0OmTdGLLJ0popeJIu2wWVAyKZ19YfvLQ6QtIhYkeYng4bH47Qa98Ze4jMnSKbjQ2LtPe2ZhP/NJf6UIXHMPJ3/8IQHgvHV+YZVxRIWHFrf/1asvfjGFx79TV16UfdA2Ns0oVdSkk8PTjpbhD4kWn466/mdIGCK126UDEAAAAADsfMXQMwEQQODTYUDjYSOrANDNkUt2IgwQCmoShFqggKPpNy0tM/jYnhf1lKDiiSbMELBQDCa64M1FQ/cPjAcAFDRAmdiK61DaEcdAxuSyrV87OUIvEQ/fqz+XpMwIJh8OCv+iP/X////y/vo/N1W/QSE7Xi9M5Edj/VBYYeQ5HHdsNAAhNQBc0zIroqI3MaFhBsIiEMWFYGq5aYsEIglep+NngKLWYwELQlnCI9nFDx9qVGiDl8JdOr6XgxoKgKoUCVclK4tf/qcMAOEQ7/yqGdVXNxwI7GB80X+kVw1/wMMDgP1+2/xpKdirJGLINFxO4tjlx21nCiGH1uPqsp8p3y8y+WMCMAAyu+PgMO84cVgi+BkFsFACDqscALlGQYywZIFnL8ZVlW7cB2X1eSDkODJpOoe8y1ZA/T/+7Rk6YJEilBT21hDcogsCt9lhbYQXUFZrL0SwdovrD2WHtBKRzlau0rAdBqih5JBy/DQ2RKy75rtrCKFBKShtjdx9RcPt9ujf0/////8983unUueWpcpmWndzVWj/Ku16D5WUIIAAAAQIQAwcNVCKEEwHka4dNINAQgFJlACYQkSsYeiA4QW2X26zFn/EwFuF3s/sNlX2M1VMNDRWLhsOT5XCi01ST9pr9dKszpU2cyliq1Lf/ymdlfkfcPn//9BYIAgfFMa/jlGREVK+W/9GGjPJN//os4fufTv//ys6wnii8kSMVkIpJ2qI8OQjCiZE7I/Pd7vpbUMP9x1ydARAAAAAAfbrdD6yu0sViHbix72CrF2XbDhO1BJL0umuslKqRrLeNwQXg8YAUBGmwymuJXD8rkjIGWypUcd1KVx3tUsFLliMBQxduTaab4+WaOoZDQjNUXdm5NFDE3Bgf7tvjghYCRvjdBv5v////+pCP9VvZjuXCBHdi0bZjU/R1OZu6AGKDkuF4DKEj6BaJqKac4LxlgjBXOaBSS6wIhLKyILU7f2zSUEMwhFCP9sQUvlib8vuCREH1f0caeLv28JhYhbBrMP1oo/mH8DQXAZib/KiSM2R/oJQskZN+1Tkc/ocpESf81ULNonUoKpiFiZnPM79U+ruUyV79qr2/4f9glK6Wg1AjdNywYOPSu6+jWG6mDCtqFitqVKwTAFsoxoAXYTop1lv6mdE2HMsdhZKVojqyVlMwGEYQ1qVRqBYpL/+7Rk7gZkyVDT41hL4IaL+s9h4rYP/T9VjKk6yfMwK72El0gqCk1HlW09TDOL8tGROFhg2fNHmkG7JMLl110f/v9xgKUX+rdGf/////t/kJ+VddkoUDsfRm2R7t6CTyDm1Mw56pWAAAAAFCBUgbYG1EGFxJWoOxYbnsaMCKR4gAiFCIAKHQVAtCBUaqe9GzLISJk6Z2VaNFgpCgvEIgTUHJa0jJWnArPakkbzjAhCEQLEV7KBtZcfevuuGsGvaMI13u/+zIMKWgkwv/7BGBADQkNf/+qeg4p/m7WEH7rZ8Mh5pSpwrTNjejcdoIq5QLzUqThOIJxqyqRb1viddrfek44+Lq1gEAAAACoGlUVQ5pywzQ00kCAj/YwaIK90JCSKwAoIPZOiMBExKwiI6mxFQ4pdVtHSXeMHhkqp1EFJI9sPHpCzSxCzBT6GC2F4VQ8pTlfYQ5iNAXEwBin+TpPlwTihNRg8RXDOgI5sb7//+U61SXJCM//1r/9rp/////+/+//bJe5kMr7WzYMtveQMBtsO4wt6UAEQAAjUC5x+Y/AICNEUgy4So4CsdObMJ4iYhby5xJ91OAMskCX/0ricB0L5TNo8VyagvDx5GAoDM3JxmOosv8mjUiIhgaf6lMj5v+vNysdTaQ//VPZhP+qXIF3818PpCaboHk0ig1aZnkSANWBoS0OSz9fYm/qpmlHogICAAB0TOqYAwMMAtNikYrSPGQS3WmLMVvXI7bqsBEyTBLnhO1CrjoJcbSPAUFP/+7Rk7YIk+lDTY1lbcpDMCq1l4rgPWQdb7D1nyfCwK72HlfgH+AG08Xw71C0JDadhIcqG5zY4ng1UF3ySHKgocNRvELZWLr79PU95d/X/hg4BREf/1I/2/////9ZTfn9vsIEUtlbbqreswg64x1HNmIAAAAAAIB7aGGChILwIJmMTB2huSPLqoNuQCJgTS1h4F+FyOW48GKuLaQGvS3qyjuo5KQaMSGwhdcZnc7fJ6i2FxC8DiFKuOV7v/BdwbyqFEJlD1/hPQNiz7X/nzmKEzl3/8lh0OI/y5Nj+f9ptVQcjEjjhgqJ2CHESD44OYwR+R8oE5hN60QAYAAAAAC3IgUj46oyHYSMfI0rUQAIaKgN6sCw9PxmogYDhklWkpW0jDmJFxAoi2yGixVlFUpk6FI0PNqZN0YMgxToPhUIGUvJwMmrPGpDF+GQcSZSljGCdBPW1FyIYYKHvcQVd/v/xY7Bxv+rf0/////6kCaZdGsdKM1Cmc40SM+hG0/7ttQTGHAAIRLygsEqFGD+hzScZ2QKOOMiyXiJEnLWQ1oFLL5eidULtrJEBSVTLWad6/LAS8KHiIUgaduGKP/+UrHlq5lNVwZvvW3ysd48BOAQoMpB9nJEcAxG+lk8wJIly09+swKRu76zJyWPJ9/U/qKi1iAgFLmz6EaHo7Op/KprJNLbZygQQA645wNCAAAABTe9jRfkGpgdxkUvbGY4i8Fg2yAohMtIgvI/KqKcDY5lZtqlh6C4g8b8xJTtv7KQjoPr/+7Rk6AYENUZUay9FoIqL+r9l5bYQtR9RjLU6wfswLD2UntjFVCi5OUkq5Is2SwUgeTbQkpKh0mJjUYoC4XwXuBP/crs8Sy4Tobf8pb6X/////7Kc3/9NEMZFu/Qt29SZBhMVdD1OExJVcgAAAAAKUSFUoQKf8vCECc0x7Wkttfrkt2AIBkyGY81g0EqZulp/FkozAUGvFmAhRfggJBQ8oKIYU/35B4CyOjGOhlVJ9Y18rNESeBOHD//uHYdjv//EpA5EEF/hLxhRwz38XeI//R5qKLGqgsLIaDgwokIhNZVc2HAoyn/E8f//yNPRnMPAAAAAAAHlVnieb5qCxh03DP5tKUqAphqiZWnOnoEQgpJy1MQwBWGVMHXUW7Lku2tppKliELlF0mBINu7F3yX9JHUm4rdoG0d5v6WYZXIXQd9wlPNPtwhw4rLocpo/Ya6/VmP1a3P33HE5XCh4sID3+f/E3ZP////9XT//8eIXZV/nCIXjfLZuGAJM4LDtWmDSZDdgoEANq8R0B8gdlaCNBCRXQJhTD7FpL4dwBaLsWIxUc0MRwyF0UCsLm+9mhlYVKS4fCPXUD/V6q5mFhOZnhRWR18IxsaXAOFn5Vybf5ARxg0w1NFU5T61TCpFjTW6KrrLnSLYKSJkRUqVjbNle1vRDqaklf+dV3tr//9HJwc4i8ASPCa7k6ovGOwzGQes7bUVV0133R6WOlyIBkvEcGpK5DkcggoJG0cpoIVCQcgXY9CNW1qGxGupWyGtXHpX/+7Rk6wJkLVDU4w9EwJKsCq1kpvYP+T9bp506wdooKzWXifiFFiRLpdIR08pbPUCSFsa1ExLEjtQoctyv4/9f9lGIQzfV/6l/////9HRv+hPVwpdFhzlhUEXwsZWokhIE9hEg+gONAn6F5jO3BvHRAgzh58jHKnX9ALrwUtZexigDST9eGC4AmLMcAr41BcipcT/2YAdCvANxJyCgtiwEiqOpVnX4Joifi3JQT45///20fadVGZv/eHaRlTUZzcKwNeaWG1se/8zf3TTZV7f/4a8w48kh3s72yKdRVQg5LvkP8R99zyn6moIaPVKEodwbaRAAAAAAAAKCiASNM25AInZdlpADII2lrSYugNRqc8MBhBUyKNhw4UIo5VpUMaC+nGQHhhlkC5jzOWiAqPRfJuL7vujgtSUMtobklbdH+JzEVhlPibh9uIQVabAIi/rBYjWqw718YGfGFXalBe//+cICBQFxfyEd/0ZN/////zDrfrqX1GlFqfzP/rmEhBszRrPJASvISUNiR4gFKSkTTkpaJtHdWK7SO9YGiV601lh+o+NYvRpgQ2PNMo8ytKsl4V54UgqztzLDcAkxPBfP8zKfUXckdUGihMF3//3Ixgifyki5dS7vzfzFvfwO+CQsOGGf4zUfoLiJNOJyA2YTBSh/XjeRxtMa0BlxVJ0IEXIzWVmgPfOcUMGSudsucX0ZeKTwwXkReMdZXqWEQXbFFSppuEwtRpMcEwcwM89Q+ClSRpCaA20+TeLFVg4U8rn/+7Rk8YZkoEZSgzh54JGsGo9rBX4OuRlZzD0PigEuqvWXqpltlQhQJ5VqYsTcVilRSsZswUQRw1Buj8uPS3yEfDQsYbTyiFP+/////+qH///serf6/9UxcC6vLYqUgAAAAABxUUESC4nkGRLTjpwnDjJWLwwjwNcR9WEICKcrwiC1I4kgu0QAaW1uEbX4mHOspZMFTqWPnEfupF9EH4r0ufTuFBSiucZ7sqybgYjNJ//xQ5jQ7T5i5EMbLtdD0qUOtP+3eCCeZ/4050vRRHEBAVDUgGhb3xMHFhwLjeL43ezKMqcXv6NgAAAAAAAQawkBSukXo3LHgPiBeiCRXLSFooRBYsDFiMk1AzTXYQRHsZSyVQJsg4BWlUKG5hawNYAJ72oCBI1lbKnZcNcC63ltGGXYGLfZ3KxKrd4ZqIWZg5TXOMkynWFw/qdiEPXrLnX/8o7EnOm+iufv//////qg9/+yt3Y3daLYv/5jIKghOIFxoLrGAGhOOmMIW6IPPwjMsGC1NuqlH1oUAYtUaWLD1VHGbyCay12hMlj9eQ1GZQ3mwquIxujuuPjPOY7RN2imIEBtcv4dllQ0QGv/yreqr/cyRGEYw0VmC6kxhhI7/NPYXXn/9Zuun4PyysbTm1d8cnAtFHh+OdXccLnTBRgGxH+j8BlMzWQGAgiTV3K3CNM8HCNZVwkmmmjQQnjQQMBSzWyPJuhAqGjPWSFzUgGFprLVfpYpcdDNOtiimil+fH8UzK7ah5vYN9qppMl+hyn/+7Rk8YZkTk9U4w9FoI0L6p1l58QP4TFZrD0WghwvqzWXltkSUyOuQo5oq9dqP9be12+///oJsMT6Odyuy//////9SB9nLtH1KIXFlSIu1FRXZUFv/OinBB6iJhRi9DAAAOPl41NPItMCFjBQEHmLDqaspC4Cy3IMeNtDEGX6qm8LBoNSUeVt5XHJ3cXXDTlUhBAuqarh//3rWMwHI+y2uaWYHH5RbUbz5gVv//p52lK/6N1SUCeT4Mza+pNZWY3+Yo+4uTj/9Tb8nJpVZUrg0JbCUYV/D1hOPv1zuv2fH+vz7pAAAAAACIMaIlazxrror4bMCYBbhEFpQQDZOYEAYwAacaNNgdAMGaBBAMMrIFQ7Rn1DiyCUIFiMcKIjACUrzLEC/r/yVSFOpEirlUq0LVIP1Rlcr3TwupTnuwHWoi7Pz/ZS+uSyvGUrRaD9bVdPub/+gCyILSPyhqTl2//////5Uo37a/1d30V6Tf/Kjhw6E7nGKN2IZQJQgBGpSAKVDto/CoG43jyFdyeSxmcTyfIhOT8ThXIo/ppyEjkFIaZZqGa4TDTPogx4Rk62b/XTEJEXqA5tzbFeuHMCAMpbf/7Gt3s/8wKUAbPny//Ya3pvffNtTPnGtX/97XTKK7OWNOmhKNUTQvRh9RpFL47nmftdjs2yWmAJXAjhIxsuTysvCMgG1yhOUgoeje0ESKC9wtUM1nAWFMjp29WDBoIaNHlLHmFCI0msSVitxrowZmD5zy8Hbg9qbWqsVehNqH3/+7Rk8QRkI0/VSy9doJUr6p1p57ZP6TFb7D1tgi8wKnWcHfCtWbb+OWq+G55piaiVjXou/datbPCYCAXBEqNQqRLfG4AYyPnN45oWq3q6T/////8/P/0/X+Wen7c0djzCMOGHzlH6eEBEAAAAABG3R2awaQqmAKWinDpmQ1NR9iitkebUKFVqaXNPPZzycdrxbMAhfFCF4B0RUMCdI/P+ZCgaD+mfhrTvJqbnbIYmf/ua183/7CKCAINY0OX/CyRwwa+/Ygcn0L/5TiZas6bY99kodiyg6g0m9ThpDuLP5h2zRCsAmAAAAACYOiIAmOfBnyrBEqwM4YFK0832L01XwFakSwoaaJY8Yjk7jSFSs4RREgWdRh6S4aaGMC8FvMtRQzQTqr0pC+dSFhWk1RiRQ+rqxkO1LwXFMoe6eOyGFoCcYy7Gt8RJOBGIobN5dsb/Qxu3////886s6i2SxT0mvRT+pjGHu/nGkR5rCuTtZCxWhUghagkcTWKhghAuQKATL01DIAa1KwoAHAgjEkUMLFwMpk6K8izT4MIYFVQOErV1DSRzBG5oGJaIzDQTIuab38OAoBpA/QDI6OoJY8GNtiJqwIEa5o///wS71rI91/rpIwDBx67df+9WgRkhfE5nFjKEh2X//vYeLaj9abcrFshKGFARjKUoJQE9JTRAd6EuVrlwARLTyMQSOa4iBhC4FNMRV0WvTDUwet5AYgQSCAxnFOFtFTsvFnKDKjXBOrlVGhgCQvOgq2FiT7y9xnH/+7Rk7IZj3UZXewlckI/sGs9l6qYSIRlOjT02wjwvqz2sHbmhypcjlZuTPXIlv256mq2LVVfjy5uzHq9uD0JAWBIA8Jxk8v8cHDQDheaVPRnNzG/1/////9TGU5attR9+pzmzTj2sPoUKPN0RDgchOIBlkQRQGpCGAAAAACDglskjSIXxtIBmZDSGU9XsgRhRcxR4rGphHy7KusB6piBv7e07dIX8uxLzr6gk/xKrZT8KNZYmDECB2B8p6K9cuX/8OiJ/TRxgIOdR/5EP3RSKKf7PSQjKJCLFGjwgOIPCTM86h0aylL+Y30gZ4d/QVIAAAAQC5VS3jSoZmZJcCbStMVYZWFbLEwoBElBMzVI1XKSTvqebsohKmoO211PR3WPvM1NoTQhKbVQpcDQqC4YRO6pEjJ3SRiNlEDmIiuJHRtfD+x3//pFFnlLkv4sQ/l////////N/////OQ1P5osCwVVOcVc4BhPR1EBIQpWwjInwbLSBRC9kr2ehUQkYFaxQiEZykTla6kHDYYnAwo4JpWLnPXaUBmakI00KAyiBO6PN8sDC34tOU8xhgAgA3nXa63NUUNZojcUxbBGA7hfBlfj0DiGsYc/x+XSIh4UkVITP//TUOo6nTS7kiINsT/9Z1viykApGUx54rogESByMn2SFEB7hB/y6JVQUAAAAxrAw6HHXOQqcOMJyC40DAAMPddFYu6pWW3HmIBTq2qxIA18P0oqiYFRgCDqYJfMTAo8LBgYLISJcRXs2nyCBXpz/+7Rk5IYjrFDW6w8r4HiMCv1hJ7gSiRdKjTU6QkEwKr2nnthHRWNqMWGrN0jm02xHNdHyZZWHQaVn0BvdncdRhK+ePm8bW9c6aQGpJyQ86F8qW/1M///9r/0MI///qlXn/VW+tB4fBsiP6jAqeomEAAADRRdeCVeoGgkORFzkoF7iACqSdXQWrGVDP0qygKsRP5+pSZAICh6ict/9J+F7WxqiVkBxVlMYjTJ3vf69XjasScEONLzgB93Zi/PiEj4r198//+LhYFxH6GaDeJA3UsS/u6En1HannfsTPM9OWXNg6oDiGEsLyJ4mdvuz/hyLcGAAAAAACoWRBN4YRDhV1NpAC44aed6UOprLXhUCBVEaVFCwgYOCQRvhGlfsweFOYuw6kQMgN5g4ku7cHioGiGehRiKlpZGo6ifotLvVh8bzaaul9ngJOijfNU/gH8O1XTvlualZf1NYShqVQfZ/VP6f////+sv//+qV/yoeN/mT0i1zhdqMt8QSDF8jWyigkYKgqBw6B/SI1jzq3VKlgRxYmZbqJAPnDEggoQhqLl8u8/4ChxwVbgSU8jQZBUbi+cR5tRwRlrSdte2ocZLdtYlCqFkGRSX/JRAnkY10X4MkCEbRR///xkleO09Ex339r0mvpeK/IqIwPNoCMSQKR3xpLCh/+B936BySgKB4dUcQ1C6V6Qw0p6AGwa+Fx0KrISvQR9eJyC6RbdOdlsQREd4IWkyoahUHAWgzaCQiAEQQggXApZJzkNxFMasGyJn/+7Rk6QZkEEZUI0dPIIir+s9l57YQSRlTTKjaQgku6v2HitkdZwKrTMQBDCcsyicpGw6YK4cFUqERHJshMKzZNr5/0UIXM3o/6XL/////qd3r//oqGXf6hX/UOzjvFFaR1byGAAAAADrQMAGR2W6jiDQDsHPGjSNDm/EMRw0sLuE+HiGhOOxGzEy8yAkepT0L8VGELRTXHgHR5uTbrOXTQNXt4w+QnBp1M1f4MKkUn/5GRYKwFS//fBKHgbIPfBff5JJ6HK3/zTEIY/hya62+fjbF8QciIOE48bmrS8zOkhN/OogIMJiRdSeAdn9i9CYQAAAAHy6yYiu4KGM836fhzOZDmBbRliQWIAinWPJ5Ajai6KSKsCqVrTV8RSZeClESwoZmwVEtQFXQBvlKLcpTGFyeqJwMETIiEBRrSx7J5BIo6DyVCHHcr7bxHYiHnWzNmb6/a9+igWi0PXMH7e5//f////+iEI+PPpRKbdKKQms1n/97KLiwrOYcRqo6cPleFBkkWoJ+sG2QiAEFNx65sQvIiU4iWyyiQj4XA03VlC3QDxKsarPDV+HuGYyQHIW9HKVcb8u83djJtbx40/+QHnCkj/8bWIQ7/5/w+Q8+Tf/GkuimxwMGCgelFD/jUV/0XSTSihFGlYdiopy9qKABg+QP/uphZXvldCiTQz/srFBSeMxdQ4xVKzMEpVAI6MCEBrIXCZKv5hhZ0mDDhC/RCAUyLeEYO8zilLkS8MQuQJkZQAjJQCvW1aPGKkWVUzL/+7Rk7wZkYkXUY1ha8JIMCr1h6rYP2UFd7D0LwhGwK32XnfBF8PsdJqQIKy8TiPeqw33CCnFQflZkElRoIpAamtlHyQ+JR57ovxuVf+f/////0U05fXf6amH13en/1JIBVI2dhqQj6jkEAAAACnqqhxAAEKD0Gy36Wxx8sdRUaU97TWxGKSGCN6sys1pdNMpN+GwotOXGpU5LT3aZGuwdKb+qznkYsz24Sy9DNGuExONUtHNl+qOwnE0Gi7/Iq2pf/s+KKh4JK//+qqtmq/6iiS55V08f3/f3Re4+SSwvLCETZV1CbKEwAez1Fwl0viwoLZd+dR4AwAAAAAAsFIKJru0gJTUHRPACEg6hjQ46WalySypRaaiSOaxlmo/TjDZUyyEILI+GAgyl42ECzi5qQsPORJ2JUE/VLUkWBnHwdMd6uHFN5VLCoYUEnrWrVhmhJg0k1Fi0zN/bXmDwOgb/USI/1VWKn////7u9C/X1bo7fej//GsDEqsYHCUoDCYlbAABUyCEtsaIDrimCQZMKxViTPHLM9tSxYyxXDYM1KTqUIcTECVPQdfWAHHpnrLBzK+499/9daI/DRXkZTalsvl30IfYF4kjwE381tvlGj5YscOJ/jjKx3VB4VKNCpmpynf6ldJYiap6E7M1ef5JJMTnby57hBuyujNfXHycM33EIHgtZaKk8wGD2HQ4HGTGQlu6JAQfTaOQhrwGialAwyPMuaagcoYYwL7QuRxZuSxCTj4UM0kR7T9pEbxuEhJr/+7Rk7AZkZlBU4ysewIdr6s9h5bZQeT1VrJ06wg+vqrWHltkmDpH+oFSYamh1L7AQhSR448zhejAJMunFiXI3kMgKNRNzuJGreLOFyAKLk/nRv9S/////7Me/0Hevr///UistehhIFr2EAEAAAUQ67RiCJ7GAgWdLgryBHqYae7zNwU1Wgm+kGleUHt7FXmiTAUmy+K6Yzm8SjVeQpvLMcpk3eW4x37cSjLsqZSeDJ6GbsPg2OEgQAH//xjSkrBwPpYns/4OOff/ydWcxkX/ur/b2+Xn1DI5dE23zNNYXk91/DVx9/u5uVnPdZ/MWgAAADwsna29FIw1S8o4agPGLfLWhEwcGaOAJOPCw4LzCYhY3F+QxiYIpULvVQTLQjEmojiBJ2YZwojp8R5xFrILqCsueJpSZMQEopXyWNQpmTKGKLIgdYWdhyD3/h9c78O02ia0ZZ9G6WelfJ21/DQqLhsIBb+pyP///////UvLdo4fz7skz///5Zs31itiIAAAAAjJeGPRomAoQpewdVEwMYGkASKUISeaMYQGTFBYuAQCcdEw7cqXUjytRvK30TpKC3mskgyrGcOa//uUCIJal6JHTdb6A4tVgNCqowJP+jc/UYjxBcTTvtnUaymlGkLfz8f/0oEckwXNik1FVza/zUkStoP/bjc9u/+NuYRVSqtgRR7ExHBdZrp1BH0g2wCMan2LGvhYAAvGBQgUCDqGyMuXH1N0LWuqyqGAGBEdgRIIIg31Yoi6l/KgThTICZEr/+7Rk7ABkK09VayVekI6renhnB35P6SdTjSk6whkwKvWHntCoeCkXmKckBLyX0fF+YmRdyN0rEFgdAPACDE8k9DeOkwdv/+3//////V2MWb0ZO3of30eqn9W0RhUNx8OZqjYbEUqYhgAAAAxRUAGvgEMCSiqCWAUljWzLiEgrT2qJRgLNSIcepYzaWKFu5PNdjwcK8lL194LeCaIQ0rZ3ArTfpF4YgxAQkpTMSgaesijSI8YMbP0zeYHuv1OhWej07336/rJMZqJluc5O/T/976xfaaegiIbOsrvknPaxG4qHZ5t5Fc51HE+/62lgQQAAAAACg0vcDsUyyyLNHiZsTimQILEMDEQq6CZElqE0GMgoABHDeo7rYKqGioUiT2AP2ErMIA4LLAqaLoVxV5lfI+VH8dCtSVWsJlu5KpRC3ekDF5Deh+djD8w9XfqnEcuSFQpGRON9Dn0FYtMbf+e3r/////+cymJ72/6n/1Q0g9W1QupYSQjBFZUWAaNTGxQYwQa47VMy+YHGzsvqyyHzGpr5dRyJc1xxRUCw0gy1Mm8/MAN8jliE/oejwERoEV+iKAQHhQQGku0v3UQwdIE38sgmD7DYqZ49lajADWlOyccXd1RPmyHQ4qJ+f9ZtBrwPEQwOg6JDsPC7FBdpbcgVuzK/tf/+EGXVobDADEBALW+1hOROIaRDDdoygeyRMJZy4l4lgVGGJgFr8deuWtnRpgxfrNIcaMy1D99fVtSNbaXWXFodyi86pOFpeHVl47H/+7Rk7QQkMEpVYy1NsJJMCq9nB24PcUFf7DEOwgKwK72GKtD4IVG3zG4Sji1liRRWHxdT3pejBmFOJI4QCoX/kr/////0/11N/bv+79nc2cVNdL9VZnChJnZSw/Kk9VUCwAAACDoMiRpDEwIhTcrApfHMTq+LgJVggFDAKNktBW9gr31YIr9AABTBDhAKrrFthltsi6AxOPDmbHhaRZkin2L0NSNch79JGKaJ7W/PkgCUWzqcNf+GGo9k67/q4siVPFKRrePTzth5DiTHusNtx3f/4+5e7k9SSDukfYRr6dZv5esEqLsHtl9hBYS6rCIAAAAAAgoWFCqO8Dr3ICUDMY4MUXir12ZcLEmbqfyLFwMWCCoUKiNRCJ05kvmswMzIcOMYVka6kewaFKE1jpRorx5rRTJ4OtUBljzQW3FhJmJ+qHZln4s2YRpmusr57tRNlVSLCcJ8e+9oaJI2Hz0Lv+cj//////+tDSCN7dPREPdz0TzqZ6MjnjVSIgPWkSBocsICFTy2Q9CSJpOIAts7J/Y08FGQUZEMzSTAlESV4zCfYlpuUYhQdKtOjei/UPg2wIhenzOaDTOiZT8bypXRvLbCi5Z5viLJFqWBh3/hS7mc74pN//nfZpM0ar/vt4TzG3CgQ8hc1/f5752ypY8wwnYoDAoBwW6lvBADRJmnbqLXBmadomAACNrQkssZXM1Fk9TRPaODgEVGWjDREaZPYYqWuEp3KQuFmFhS9iYpjFNqHepfFs1SBHaYoVICzqX/+7Rk8IZkekdUY09NoJNsCp1l57YQhR1XzDzPwiUvanGXltnLqHYcplH0gWAuAjb0R9kapGJbJ6FrQSmOCFD2LWrX68pmVEKcnh2w4EjnJHk+0OKB0RFXFlf5f//////zqbt//7/6ux0c1bUMPFgOkTIOnXAiAAAAAA4bENBLg9BhUVVcyAHfDKX8EAC+58tgJAgARBk2XMZyycymIM4vceDM1Kcm7yHeAlrQr2WJRjKmz7MbOuyfcoaVv/O1qemz//7zSCJaOf/69Hw/zmLmPD/5fw9v8bNRtMODWphskp7/10fh5iOso/qERx7gJre0AQAAAAAAQFhkFIcDBjScysp1QYEuuYHhFBnVFQQJKucucnOKgJNoSWvl9YZT3EQiz1Ykln4g16Ug1KmV3XVh20z9+8mNT0yns1+W3Jl3KzyhwPNzJe/UZiTR/2VIvj1uP7v1mbjBMSpV/m///////msW3X9Gpf0vqom5HpKhzkBwINaHQ+QeHYpQElPHXh6BZgBR5qICRkRRDkTaky1nNIhxoIGHpZjzxxWw1JiUVWSLCMthOvaXCmlus26+EHsvrU3/dvVmXL1eCifKYv/9ReMhMAWLxj0PPsPlvlHeIpB1/R5BzdCpKRLd0utMx8wtPECZZwo8VQa3+FLFwcmUg0Gj9cDpw3uejADQL5IuCRBCmZW0GteZMOstxCDVVUpkmhYwGTjy6wAMAcxSZeKje5lxMJEJcge9SWTCEJYqGAjWyKXPbDTj1G1nZJTQ+qz/+7Rk5oZj5EnXey8y8ImMCs9lhdIP6SFVzRzawjovav2RJ9mEz8Ujr3QQ/0zDU3E3TdaUvC0ynldLE45B8LmMu0OOH/6uCGI41f///////5TBmWQfnf05m0pSa96IWt/h4QxxChE0sqZMWbmIwAAAAEQ6jcZ4bsGA4WxX6y0jhEiRCYkiVAF3pXA0UmcfB4kiu2txGEJ+EGQvdFkvZTH+AXDdEkaKY3SkFBQSNgAUbx0sT3f/yvzqoxj/r/+Q2JSFEYd//mFjgvYn//jLKIb8kfLR//peMN5lTlCErLDoQBLNp9DRc+D0IOgbYj1d8ryrkGWTNL/TPAwAAAAAA1X5JkF5StLXFzslJFGmhccWIhNHRJ6LlDRszXWwpWFDxTwADDBlmFRJ2NuKBBDRIxUJyHF1hIDjQHld9KVsz7uxD6wYjDdRs81PPuyKBaj6OO+8Bz0hiTdpuQU/VYI689JX7/cf+8o4ND/////////spjNajKpRvtWa9msa2o9VF2OdSoRH8qYKCCxJAqAYAFivEAAOouuDowaqeLgK4Os+CnMBOUoYVBtQWqyPC5VsQxUUQyr2Ov5OxlcsZcmrSq9WsmoBUUCqHHC+PzE+gwhGf8xR1za//wqHcamkwWf+5ZFsf7Hv5+G1t21X3e+8kWxK2FHGqe/BaQklH+9I3+PKDoS5N0h9cCgABAEEIg1sdlLOHyaQFhgZcJRpf13EJ5iMB3igAMRW8ZHBMEhzy4bMoUtJVAqoCl0kwNhRRAyTtMj/+7Rk6oJkX0/Vay9D4JHMCq1jJ6gPmTdf7CzXQgquKr2Hltjo0pwB0yqk9I4cKGGWosHAYr5hOA8zP1pUJtXIUpp29sF1T7UtXjT//1UBBUe+L/V///////3KrO3rX1b0/Vnlq31EIiJ5RxGJYDgCQAAAFj3FQjlNCqJZ0wxWSsnMQJCgcIMMVO14JIVA3Af9OJpScMjlU41Vsd7G3SsKm5S4MMy/8cLW7tns9G28n+ZR6tP/mjp5hFvyxphb+hjlmZg75YsMmaY8KRGkv9B8o2G/TUJgFtgARLsPWVk0oxR38MOzxETb+C1TqKlgAAAAAABzCQDG1X21VljnOkLDERwKUbmWESwmCOA04zhBGekaNDmIilOwdN1aCHQUAUuSoNJQ4wkE5APKW8aXGFgWHKCsyjavZSwNxERnMoIy9aZqpYR2jnUqvgjnMsxlREgnILOWI6Wluaqf0+4cFBcEZRD6v//////+lmK3tTuvtV38uju6VfE3k8yCkzQgEIAAACAERcneTlO0aD5VTMwZ3zdjT/UoWfSIALogPDCmuyxsdFWlzV01UAkGLxaU3sdfmOItDoLDmz2Y9PT0dsxmJkAkfhv9xCZudyYjACER0W/QgXMT/CImJ0LIb8kiu0+o5Is3+jVuT3dwabFumYUmrXvFDgydEmxFxL/Y7KgxHEk1yVTwgABAlIRHBQqTEgJMKPGoeHAJsEQOSPMMjFiVLAkg0wEu08rCViK40mqdsRiCKiAEgCEEBLcAEWljJ4T/+7Rk6gBkBlBX+yc2sI9r6oxl5dJQ+UVX7Jzawg6vqv2WFtkRMhm2DES7gYChef2wZG5JHk+BmKlKrpJzyGsWHJIJ6+uM07f1zigKdhAv1o///////52T3a7WdCFYhjo99vRu68Rcp+VQ+MWUAoAAAgAsTIdy+AgEF4GxjQNLcykQmJqbJzsqEAQBBRouDqSDOLAGgyG6nokqPPVhZZHI+QlUmVbSgcg9UhVXDnd4Yx1VZXHyKlpV7QFyVGRFAPAGYz8bCSwp/zgoJmHU///MkzJk8zNgNwKNVlZ/15r/3C/mpE9GhHYmHx6nX+ieGCAf+V/NN/89jFkVBsnL/6tSAAAAAADwWooPLO+zCaxbgcaC+1aHhZYWBRUwLLGMmW0Dm2jl4mDwYn+j2yBZM8quYaANOA1IFBVgRJWFciESV83ZhEcdzSRxfln8/Y0pwztrhWGsZBOEapQOyOpYMjAL4ygvpMPRwR0caDohZh5v6F/+3////+//X9Pq3b//PMMLvqxWPxEgqCAAAIStn5bCGhQDPRABUdAF0oGLSYQ0ss8nqXSJeztsCffT5npSVuzDMlzs8eHg7zv/4eKUqcL23N7Fh/ywEU+j2m///mj0P//+kDEhgWXW//22y7QzwjKjp/v/m7jdnWyWHhxKKYUBjAstf3QKiHBoq4aQBvON3LwqQ8PDBj+j4gIgAMJ5g6acMt7WgpsgQlv3fcRBcv6SCUaLsRpYZL1s0DsTWVK6FaMIWensIltWYomxIVh4VGb/+7Rk6gAklk5U60dOkIYsCq1lh9IQXT1h7DzNwe0wK7WEl0g68kKgOdu5tHbd93/n8o9Kb0GRYFkSScHpMr2NilddFl5/+JnBRYBYu3+///////2QjS/K+/z2Zf0J/yEGmDj6qKDXeAKAAAAKOKgBqIWSCwF7S9zOArIZqmmoYsUQFkGxkULFn5ZWlLDVeCXWXqg4iI0ZwmEq3JxvIpSpQlU62X1ufpv5UkYISiaDTok8TEIAsfuGGfv66bfTv//qEAsbmNGAECUNTR8t9EUokbKYw2YsVM7bnnLP0tWjacbMJDVtQfNRud6J6p6erY9L1rngKLdH60kwEAAAAAALB4sDRGMRwYd6njgwPWlmMDXWXSHYqyKxB0RCRrDEGYlrn6SAmi+yIAkRpqwQ5EYzGDWJIXI4n52nGlWCcwowwAFwy07CbUOJmYR4teznY3BOqjSqc54SKnlb5c//GuEAgCjBI5v//WX////+qI5Zs+buWtFQ6FuiuoxZMYINiSA0DMeMOcTI0GBMIiAAgKNetGLojSxGm+rU1wLRlqjb6M6aMJbFIHQyk3ZWF3zxUw3R9lhajrTDY5jvN9yd7aWf/NEIJkyMkj3rd5vw4LeL//4ML/7rwEmQSEGf/4cPcr8wqtXrXoOv9iVZoFDyhQ2DEXnGWaVbClCOITigj1cN7WlIPhPl3YBQCyeqPi9V6SRkMdEsQG5iLT7KXlZjCkrAlQLEi0qjzsJJWUrGbwSmin0RlZ21OUOLGJQ/Ch1L5y7/+7Rk7IBkiEZUY0dnII7sCr9h5agPxUFf7D0NidcwK3WGCti8QA8B67sjwSUZ+ZtF66hlTdfZIWENczNcmZv0gIGQCCF////////9P+v/V1smt2QUI8jakZSj6BlMEXGEwCAAAEhUOCF1lFwaUrswzBgMy/mSgkEmVfVTYeKBDRWgnknMXxRKpJG+2gPAFKK2F/QhmeKEEwpFhiGIRX/UxpGkcwDajFqIwHq6/wW9kZSSM1f1N/psi//TzoSMQixMue///qTnQa/u21w2z/DP/k9/jKEpyESqUEhQmA9S8p0Shs8BpFAPI2+1FBR/kM9Ij5SLJNj6O0CAAAAADg8jOYhtM31lc6RIK7QdX20NfLWURQbGrxy0c3bdlXMILmPWFQBCE2eBFcqCFrhJgSBRVl7T3iWHXnCbEthMNPo1Rg8z35K6D/n4SdkS8XrSaWnFgfkx5Z3OzOu9iCKcKBqr/1/+/////9zy/fquac562RtFnnET3HhquapbQcG6OEBB3iUYNpoEgGA0eGlJ7pEqSWBZ7SABLJF6S98XctsISYarDdzl7N3n1fV+rfzl99ZS7k9D0xEIrJ//6GkfNicYi/2q++cbEgXhsd5T/+FiYkkRea38bjpL1Uq5Z/zkvtefKsYTYw8xnOo4jaTuaCcVL049Pyi9FrObkF0UtABClkqsDdqeieG0Vibgrt0nyZi9ZDVX6Ex9HYVsYa/D0zLI2oJnwKx4lEHMmRCSFF+w+bU8gkXpnYSyXRfWbHRDxsX/+7Rk8IJkwlDU6y9L4I3MCr1lh9IO1UVdrB07CeUvq3WHiqFzWxMU74xVYz02yzH86PzX/+L7yZTCBCv/J///////cg7FYMdrNRu3R1PQ/WjdV53dDH0GJjkgAgAAAACPFTQdECQgYgjyosuA6amkF4VqK5LBA1SBiwkxvWHTUfiFKnAOh2QoShKizCmZuXDqaTav41x4V1tS/9vQyvFFRNxdW4yyzL+UwdgYLRkHhfzxrSon//+XpDk3r2xTr3/U5/+rnj2K/9VbL1N9ePrcIAXXMqFHsM3hudLjbLcSQtkbaj/vjn1RSEIk5FoAAAAAAAA8OgiIEvg7IzxmEIrtEAJLHXKSbYuhJMEIynybcQHA4Z7mSJJUJMcucwQVbiYhOcIPCKi7itjckL3lkUAUQ8WiIsJVFHOHSZKsZ35lpkylKrXNXnqlkYgx6ywp9DUw2KY6583161tgVAUPCgnf+ZH9VSn////+V3LlYmSXytZ6rVj0cRX2XkKKWRxpxMGjgBKNoiaNFlhKERiUi7wLau1O1yaAZMFhGWY9CJTDbQFJou4aKrDWGvTPwY8DRYDY8kQCl4LBJzX/ePEQ5DVkOB03GP/+qGAnyKhLFP5CeRplx//jxIHLkqYszN/CD0/SFE4jV8XVzwjOkSOE4wPmyhGDsqspztqCIORAYG6jUc3fy1Xk4bYGJ1foWEASWM6SwsJrY8y+ny+7BFeIQA6TB1KUg0JI99fj1q90mPAi/YIh1pbwxdPpy1g2Oo2EIRr/+7Rk84ZklU9UcytOkpSr6q9l5bZRWUFVrD0Wgh4wKz2FG6AzEbLKWwwXC5BOw1DLqU2cWqyycgSipFPQxR0k3rPlkfAwPQUhdPHnTH49EKSj7/yJ2+zv/////mKp7SZ3/3fIDr3ukxySTeNXP/2C0/QyIdyQ+npRSCEAAAAWv5n7PEX1zF8i6b/lB2fKTKijGEdQgaOFcFWKZmlrwGd8cnT3nTUOg6iaWoMzC8kKCcwXMQj+LxhNRVczfmT//sBgDw7jv493YPRhtpQo9nNXx/vvy1bM5QmDwOSRouvU+YYAkUXAtLSb9pSnRBVizlFsAQAAAAB4Wd8s3FG6Rl3ZWwNv+Q8heODDhJHA6QpFghUqIMFLEHOQYwTQmRHhyBRhdlsDlJkgCXMhpiaCYEYWTwVcSEeKYTjY6XBhPzuetrEolObKLYmeAeir23zYf7//8gFBA3+s5Xb//////6q72//6tyu8hUaZyk2ZxYOMHxU3ELQoKhAABM/1Zw1qw5bpNIKhjYsBBhWhby5hTD5DBLnHX5m5qwoI5c0klMU3hj4wENaO3Jv+E2xnZe0Y41dWz+EIBxz4G1yPN9Vv/9Cj3d//xtTTkEDxgkCowUYXfsz5Eg5vGrPoHYgCAFRcYU2tXQwYwjuwcoMFiw8zjwEV7toCFi+001oi6hcrkUPoZI9sSWythgbHhkRfJMYwKh1QcOOuJ9dO8+kjZIla/ia6Zy/mckToTSOW3OC6Z84egF3kqmg1q0oi9ZrMCW2cNGf/+7Rk5IJjx03YewxDwINLur1h5X5PvSNf7D0LwhywKvWBJ9izjuS1il63ELDtN2u2KlrXK+P+QIgQW/6ymK///////o5ke5f//TTsus//GLKvrqsjbRVvI5pE3VVWIKUAAAAACIlekSPBqYUFSPL4QOcZac5b5EMgACzADCS9RrVQbBVspc0DZy5aGAqE4OnPgFp8UaeDTB4CHfjLbd5KakGpvsburBrzpYi6n6RcKxgIEB5Lm6JPQM6zxoc/8wHaPQGjF3/6JsgifPpKiCi7eOTfmFX3+C7BlA8U0kx0iklxUAeHFZqDoFjngHErv7NQWgAAAAGystArJAaeVNJEyDAtVMtQjoTJIGjSQpI1kXkQCSDbiCxN+/tKX+TeN4HAADkk4eHklpgRRp0JmFF3igOAmPW2RwtU7qsSa3F4fhbsMVhlv6WKv1XYzKXeeaBoef1nNq5hR3OXp3vieQA1gNhSjv4wopz//////+juS9P/6vp16tRDCcnypv1kBkYJD8YwPM7FBEAgEinESHQSNAVRAMHLakZmDxxYTktgS9InGEYDguEQ8OjzRDDkutH2upScTUEhixyW0czNx3DlSfq6R7DPsbAkISvi+uN5/+xUJgRJqT/+HgnnGjZFVFncP//mbj3XmiSyy8oUk8jvqrGidKxn/2wogQoA9BhoN5/Xdn8XIL0JeJAC1LU2gGwQMEKXkK42TGgFshH+QoWY6SDhpoQAlhkCfQYnLNxYEOW3NkO0ozrTidbMqRNi4yb/+7Rk8YJklkrUeytGoJUrqp1hSfYOWRld7DENgeYuq3z2H0mSLjktkgSD1zFTF3u6tO23yKXJBomd+Unr///////r////uh58w09qPoQUgLghL7HZqkwIAAAAAAA4sYBPtkShb0qnr/N+NSgHA5rEMI4y03rZk1thVCvqW1V+JPmGCqtltc1C1pZyPiO46HZ00h57f+/EnL2gQ5gTqNytQBD2qkKzocFgIw6C/0nDwxQQJFL71ZvlqBkY7I/4qav9h2m7IOf/DqdlNpWdw/PFqo1c5922s5DcOk9o4N3Vr3YbBA4LZwrUAAAAAAACIelg8AtSAi0ilqmyAGAVsIuAUYXKWUAxlZCMgKiVAFQKJwQBd8aT3AcGnkKE60f1LRlBcFX7PHygDJWC8HWnRnrxRikE2a2RuJSfTGKJchfn0qZzdOopGJSYTr4RFjcWS9/fe+PqKBcNBs/1NNcu6U//////upEnM3q39/VzFesiciM1HyhIfcE1F8gNj2G51BBS2gFHJDILhWcACOCIlKUOleZ07SHdQNQcQkjj0tfaHDScKbaAiM3qsYpqr9xyZTxn9Us7h8skVdJx/HqfmH+Rynr/QfDmCynf4TZY4gP65SOCECt1E/88qunY1kCKRh3/x32wnCENNDSBgujwumszO3UsTPbS2sg6f89i+9pAtFhaIZpWmAhcN6BBuKW5gHgis+CayDyLciKB4pkNIR8CpUVS+z5Qy9i44miMhcxNp0RYUprB0y566YioGshnxin/+7Rk9QZkgkpUaytmsJdsCq9h57YQ1UdXrCE6wgivq72GHtnJ0Z4OBejTcX1BFaL8qX7HpQrD1X1IeF2WujmvUkxhMx5In9WVHez//////7O8hV7N6tRh856Ws86x5R96SAkQehYXXPHE1ayAgAAAACAu7gQd1C+rQiyqS5ryrwtg4CfQwMUIEzKXBw0LF4F7U6MC6aL5+P9Pu5DQs1dkkDhzcuwZMVlbPMO7KpaIYBfFPfx51ehBt+VFq5ChopBL//4cIqxBEFPpOyWTgzBDHimf/8GPt+Wy5KW//yis2WL1TR/SNFBGegw2VqKk1W04NXL7v+OCy36TFyf7BAAAAABodLdPC/7IIPawp0FAoICYa20SHGSbLOQ4KZJpglIGsYxrnL8KqocFqJFIpCIIzQdehJYGr5Z0dPoaJRMxhkwLaVSEIWckRJ9wJ4S1MspLyHnkcTnFObB/vHInzzTnesb3vvUjG9QD6a3///+u3//////ffP0ttKDyo5pnnbYMjwXoxz0BCOCsZogEwjeIemLQ00yBZalGr0LgjKh7gOxNhhYOA5iupFjVpq0FwQI4nTv5XlIiz+M0h7nlfFvfyXis5npkyaKbCpcoH7QulA53jf/5DBr40tnFQO7/99+KjRwiKZyasdateVQAHsKFOhkaNIJmDBwHDg57CLZyKPdJkHdfK0CAAAFYDNY2RqpQRHUOyPzMBJDRS5LGjCIQmTEBjEjEJy9C0TYy871KAhV65HeBIQuBmAphKFOThOP/+7Rk6oZkh09Uaw9eEI5rqq1h4rhPbUFZ7DytygUuqv2HlqChd3o9DKdiySoQMlp2srBZdqwhbxEFIdyMbYTa5s8kJ8nD9Vb6qt/8vwPqOU7f0b//////+R/6/paz/89Xl+YBAcODgHFVVHAAAAB5A6WZBBTVyJsykAsy5ISEiuKjA4AyqDMIIoxG0qROlxVqwAmeZoBMiriDpzCCEcmaSdN0MFalUZCnWt7KgijTxg4GDiIh1mlxBykhm9lQScYcjghAwhK/OGocsfFjl5NNEEFkAqH02Lf1nP5sXWWjWga6yqYoZQN5JscD7JEdLtC7ko+nYLIT7Xq3apwAAAAAABwYsswwEX0CF99xgYI9GQUBqeqwLhmiyBhgcAcJpCQNBThdJ9CsRJV+VhAhVfK8hCaCEGcl9FoDAN9QGGLCBqmOMgYZSDEK4F4UxzRD5HSJJKYQhavTx+zEwck1pgYmKYsbnRmm/g75JSoeIjz3+jfqe6/////9v//+9e+lM/1ICgaEywisaAUJCqTep9JHstAxBKEdJycDL2SAphjhsHiA7JW1kjPl6RPKXKCvIYK637NYYE41VkMwr+MUEMv9W5QPzJjAJFoC68JorVHQXe6gGA131Ksn7//AKzA4EJK1uENMBpI9v/9Jvxl+IDhRL/j5HUQ+1yMQdBBwiQY7w1RuWKQ1jR/+r8o8oYmIAAO98qxdEvOg7XWCaUKBe1iaFZnHDyNSc6hBJiPl1DrOgng+1GaRPTlYhUmGCuE+H4f/+7Rk6oYkgEXTQy1OsIvrqo1l57YQaT9RjKD8wfCuK32HqbkJMjgVaGqAuSiXCnsOc4TymX8PW1UqOp7t75W6SL920IXF4aCGU5P2I43Jskf5X+lv///nqejb6L//6dvs/o1PUZmCDIzVqpwAAAJYIOZsCME0QFZSBYNtFkispramBVUA6Bd4MVFQSgUvuXBRoc4WAaazUaIeaWwKOpK4L2l3VxpoEynV1LXu9fxIxgANOL+uDK2HSyKW/7cmYMQ6p5NhkXf/9MmDIwF/+85cjgpIA/hmkGf/rq1uJe82kK0Pc//nbWW17tg10DZXJ56Ja6A39dHS6IvoSOZXfMKGtAgAgAAAAADKggSh4XKL0vu2FHsFIVCXCSNXimmU7GKoYCJJSsEAApkInsL3LHYOPaSQDpo+o+D+kwy6q03mSfeB4Unkn3Vhbd2LCuE/LvR4oj/OhFm8hS5Rg5UYTA2UpIu3rtPEHQFFn/5tTxERhuJfkP/t/////2Rv/7oXIPo23yf7BQsBX6fkEQCAALOCJ460VjBY11SgFsRE2jm1FyFrWi7BWIgMUPWo1lQpus8gOYXeeRptnN0n3ceWJFJNrNqKwS2j00RxJpd6jWq1JZjU/+LzQBSQyQ+otF5wkPyiTiJOni3r5nVIrmZgYt2ka9F3cTRqxA9yFAaLjA9abvpRpw/V4fNLVDqCoIEALmZ9yfEwrZDT6Kdp7oB2QpHCNNOXbZe1KMhh1RLNdqWrVfdIdyGd1IIUAYk3Jcq1FHL/+7Rk6oAkqUfTQylnIIirip9h5cQP/RtXjJ0aQdewK/2GFth9dAlJC4qAbNn0JNFlimYnj8Q/ryqpZLZ4kcsvZJH16ZnLdKlEZNf6fpPZv////3Vv/7oahaK3+X/OLoBv8LqgEAAaUWAIB6waEUHDBwjCh4Ut6TA18sKAwYwBEDGwwCKixoiiM30obYeMjRgMAyiFWGuCMW0AqAWdTglRX6KcJ61NNTqNIJGAwvx+oSvK88Et/K3FEWBXDJGa7viIp35jKp8vf/4f5JEJ9s15Tbz+09SluwTVzVnY57/KtTq6nTcUaQbDBNglbRfc6OQiAY5Ph06uj0AEAAAABQLdEQWGMGsOmODDhKTJyuag6glQlAx8ymICnAIKkGpREOshegqv9C5hCHMGmL0ix66XyZdInUOMZtJUDaOJiK0uURlw/QsfJCWdqaifQXEcgYUVYu2tRfj1OtDY//tt7yElKkxqNV+k/6f2////910b/sy6mP+1XMLzPmEghgJx0sfkZEXYYWoAKwj2husdy3PGsp7l8w5LfwM5CSwQFnrHWgOMsO/da0HCWSzdQVi9VvioGZX+hyXwXXd1YVM61rOlqPyCKCpxeysXGnyiuQuTUVz2socasitX7z+gXy9fOX/98fR+vuZ3s//PyjmlY+SiSMUMOMN7xhWZNqvzf4un+TU4gYkAADAtYYXMZozzj0RGDXCbMwB6VclplA3zQ5LAo9Oq87rpQwEwACLZU3kWZWuVgC/ZGr6G15VYL69NkNr/+7Rk7oYkpEPTw09NsI1sCq1h6rYPeRNVjCzZCdOnK72GFtCxKmWUo/i8dW0Z1LZ8bKjd04aJAEGjTN70Dqoimr0RW///////yzfdsgm0faIg3/qLnSaw+TrUgkAAAAAoOgiEKmMuMcdDwyRlpiAhui4E0i+gWGFQi7rN0nC6b4v190uDIFhxppQqq/LNoimLAQQGSBOEx3z5UevOKvBoJBOdcm+s//hh1gkY+WzmJCMyRO/7CPSBCibf0X//qXR5Aoko4pWyyr//qSK5KWzfjjRxAgs+nn1OsplBVX/7Tz/INhmaavmZiAQAAAABw6qgJBpNJpyd30eGnrRSOQTXTHHT3LYMFS6G6S9hZuqpSEHQpnYKjGmErCEciFV6mSpAOCHiZ00zDPdPK8byoTZBxXSTvWJPI3SJRhKzgcnirICK8cyWn0xwS+FtVSfiX8On6AoN3LX5G+15qf////zlUr9GblZDZFejpB0UDHK3wiALBGBi2BgzsF1JBYAAAIbMaRh5Ar1GAUzUCKAYhJ6sA3JVI0Q3YNUZYdZUbJ4hL+OLchBP0C+1RkgnePs1wv1Ud2teWE3RyzL8aznq6dre+A+oQxUCf/4wO6Dmv5xkiAHoiu8/+MHA44qLuLUhQiINr/+DndNHdkQRmICcggI7hFmXHsLnf1P2o8SiF4bFGs1fpBMAANvFozyRW5qsqVgC4k8W5KvRFCDkIi0Y1BGgCxTsLarMYQgeJBYE9IHCAsFrVb2IH+GXFCcDiYTFNq7/+7Rk8wAkbEzU6y9NkJIMCp1l4rYQ/TFXrL0PQikwKrWHlqCogyI86h3l+JdAgMifTx8m81tx1LhlfBWqBLuNpTwWkionDFvqv8XIGgz/77f/////+qOYj+3SKvq27ExLUMFx/7hIUmiYkOFCnHCdhRAAAAAAAAAJggYHo3UGIyRjb4t0gPZm8zvPuqmXmZD9HQZ6PRkcNwQwxiQozHWhwD6H6f4AIYyVP/8tF1UhxOkJPA7Xkijhf1bWFhLlC//MPFhAdbEhZBxQwad/1IZE6qwgyfzRRDmRFg5RIBggEyMLOLCFYwEAQd3XQhSEvs6LiiKfo1AAAAAAALCgWOWff2H85GzJWxGBJhSlO1eCUyy2nPWCjJGLEVHERqbGEbFFCZilgdwQ8FCslEY29BzYm67/PozeMP/EZEwx0IjLflMP0rrU9xw5x+aBgMHPA8UUNLDsQx4XY43Kv5FQ+Bw9h3/+su3//////sSRP+rVbVDabdDf0oDY45WcAEoPjSgo4A2WIpSCRTA8QgRxGxkAGnuVBYkYGCU5/kJJJEDRTwvwZxpuR+tqHoksEhPgD8xxSNs38iLWTHVAlDTOxCVM3xmX4XmJS7FTN/+pBhghAkxv8P7MAijiU3//+dLptZ/GZk+e2//9nqiL7b5dN65lhsTO03UPV5EzjO5PMoWmt39epDJAAAAIpnSrLrSVfcsbg7yXgAAIBOkhSooumnWFYWpe3OfDtsdoIuwB1lIppLoUSXwweJIjF7lBzHSpPUD/+7Rk6AYEJlJVew8rcIjL6q1hAuJQhR1TTD0twigwKvWHntAujmJ6yEhNEypocNXIs/kc8TimerI6lw5SMArIgRAcLyQ+hDPfY4YY7/1f//////6GI6bXa7omruqaD1HMW39JMSgDThqNSKGCocGyeQJAAAAAAB6mRtCPLGuA0BKNAEGOLZQUj7DylyC5lMhNQFiyRk0Ol7GtI4OyicjyoCmLVZ4ztQktsqAu4pvlX3+UuhlajhpeoLLVgbtBnheO8URRJQ+/8ERYhhocQa6/n/aUDaMj9//zVptccrja5aa+Pm7RqON3ZGmFj7zp1IkR7DqulZV4LDJaESFWv/IunaMQAAAAAA4rkNQ8IZJWDCbFBIcWjqJ9qJ0KmrUHlVRZQ8YQGUFgNg9ZW+mZ+yRfrO1ctVL5M/eSC1otDuoLJQBuag210EwQZccWysIhzpXzY0uxt6hrRpMOcZmZ35kwlAmJBx3+hz//////9bnjistprVUkxqPuV0Xo3/nqXJq+jkTNNBghAAgCinioZZjyVCcLhsNThT0rMtcVbJc99ThQZWreHFkJGSBEk8Q1Evi6HIi0II8tZpp9+nwwKgnxEK+arNr+pVDA+f+EokZEsP+o8Qg5CosT//1tdUfvmrfd+jUtto1LI0kWNF5OFDQ+Jm/llmhm5MuBRBkbdVypmiF2BqDEdkCM80/KPK9k1hUsvR/TkVsW8LcEvG2RJwi3FzSQtZLSSAYy2iaD8ZSPRoyCYQKn+RCrfqjdnh3NrNX/+7Rk6AJkgEZT6wtOsIQr6t9ph7ZPIR9b7D0Nge2v672Hnbjurs8j9Y3mKoWymaGgqJYtEtjx+tOVFgUJGd////////u7OaaRLp9XqY093NOMZ2//2IEnYxsoSMqMEAAAAAJYNaeRtyC52Tl3EoC+bJF4sVjBfAiOOZaGt1H2ORBScoaAGVV8mmLPj9lQNA1rUTNF1AG0YxBN/ODIDjShyYZRtikAddthvP9SB0wFw+Pf8oMuslOFHMf0tm8iFZnvX/jb2vGoSUYOod/8Y6IFUkOCZQXPGjHCMPikkXd7FHuA/u/vyFAW9BQ1r0RIAAAABMFEAxSSLlgFSTMQKG8xalMZibNWsCJxTpMBmpfwtiUcqqIUA5IRBECpohAVUFAgjx5AUQHPmmSBka8OpRJ4Nq3FvV6L3RCC5kSffFnlmCXMNFWqw3ZkwTAmLs21efKqOJHtdc0W6zxY2o4BhUFR50+h//////+ilIvMT9tH01qn5k/p5myAhbYCSg6FNiOSdwimXrhxB1Wh2Fg4utqKkQ0oFdJjKVsoYSxS8tq8nO3kbk9RL1TGiacBRKThL9hxFZknGWDrE1OR4mlahk/w3Mr+ZEpON/xIK0WL3BV/vlkDAsKPuK/823/BQhjCyqh7/3gfCT6CCeJ1AWDoWEMWVon3i61SLiusbVD7s26GkgIUHeMmEnrsBAJfAreRl7C76k02mGpEgEDTGEgLgFCjopvDDq0zUi47OW4o2N2VQRFVuVwoM/bMHiZw7sno4xb/+7Rk8YZkdkvUYwlGkI1L+oxl5dIQsTdVrD0WghCwaz2EC4hj7ut5DU5E+YxLGrDtrc89U9WpuhywCYhn+rt3PnDQnY2shf/Zv//////YqmPlEe0eROzo+recBE/oBkvCtCCRYkM9dhAAAAAAaEkFoGoRJetdHBLKFRvQg6571PGRYLiNaUYSOfmsuV/YCV+XRcOLbgqHaJejfAgYsP+TsIgjKWOnRO6MBWvKZqNQ9R/YigkB8sDT/EhuSV0Mr8jA0NihZzWKnX/NrX8RDjTMWJ/+ITdr9lJEgoB26UnoK+TypZYR0W/fPoWApBTnv39TkAIAAAAAxSf9QJrLcH6SulyeCDAFIr9G4mCoU84ICI8MqZ2nQCYOgv5LVYwyGGlEjM8yhcACBERgSMOQmAWIT4XUQ9RFhGUrCAhH0IfPVankNJ+KEnu0y0Pi5GQVp1Pz9P5rNhHfxIVoX36gwAZWST02//////62dkZ3b1UyF5qvqv3/6N+whR4YyEBAATdhIUxGVMOLB4g4DHxExxkYWhL4WAV8oMd5MmaBHUcVCVMElTj67UnpWVdkaEleyzXhauyPU+tsUZ2ywZ/I8HwZGQ1fxfH3FfE6jUDY9bi/+Wn/akcs2YVL/oh25H3JYhiouHAUMMDYpAiyZsKO8ihnNVXqP7Lsgk9fv8hKAAFcosW/bZH/jpfcoHU2MVZdhpDFqQNaY0IdKBUUeVdw0XQZ8NOQLNgyKUILgFAQaILODtjogNQQzWi+YUNYLhMzbiv/+7Rk7IJkTUxVawg2sIir6p1h4rZQPTlb7D0NgiKtqe2cFfjuOK0RdgsXrSl/GgOCy9VdnL/PlE1KX7fyEylpcah9TiJ3KzsQN+V6k9CBMTG2T8b//////+qXP/6t/p/yf5xwm9U6ZfQJAADS2EBiKiggDglCFSkBGsRHBAwJxzKoZmDZHhJAXyguNo+SqFsUGjxSwc80IgZuiQHQAGB1mwTODfNqI8L1TCfidPFOgVZPnwDaL0pnkrr/432CIbn//w7w8fkYVShYI8jl//lWwd/+Pbiur3UX3/1c/DaqGUWQB8dWJokKxdPN06XF034eTNxkLBv0fTGwAAAAAAOBGfqyXWGO+40ZLsNOMyEsUeCVbjDsVYy7jD2eK3mEaSaxF5EjTYZJlNB5SYbd03VBhU8LQZbZpSJyKLSWZtkkYsgh4PxprOZp+DnKYqwFVsZEto1zJeJ1Dz9N8lGmySDjtdJcMJ5CHSmZ+r/mf/////Q5TKf/rpXr9DUa3ZxkOk7MkkgAKwgiZgAAABLHgp0q5dhFfqafkQnrLxK0K3J1JoIunrUOOuvQRAMCUjKMMLjsTy2HB6ntRQx3Nl8K2VKWK1J1Ct9av/+OofKr+VIsmFoFAGClc1cf//OX/EqP3Xd3f8VPD6axw7i8lEAd0zyLzJSLcmS2OTONWfzH83opXrvrERIAgAABvU7wiRV+vrTpoyRVNbZeFCRIzEdFMzCe5iz6r8pV0QmHad5hGF3YZUmh68LR0kmjSCLEwgEQVlP/+7Rk7AAEg0fUSy9M4IwLyo1h6sRPiSNf7DFtiesuK/2EttFguSBY2T7CUGVqNm0CQeVhGSJWThYlh5F26SZimO4H4bTWbt+/6/////9vRRqb/76/t9SX60KpqUL7ssqtAkAAAAAsSjkBsdIVBkSgoJVISoyMIMpasEgLTTL3mGTlPp5RLptKBAAEoSN6h9RcjoH0U40wHBQ1HSkWVXRYB8nkbppSaY0hA/s2uaoOFs3r/8VMEf/i1l4EAIWa6T/4r9KlBUwWqTq65gYMjl1kXFiw5YdbUeM1ROyh9iKKpx/38nY4KE3O/i1lIIIAAAL7mmFWSxhjtqpQ2o0vFFFJh5kqHUGCMyfZ0n5ZzDEw6cEp7ix2CMnTBLmMNaS+d9lrb1Z6JOPGK1SiLAKeRUsIxkgKoRSaBCxt6TU9QGygQp25//aiY4IMPExM//+7t///+y5kUqy0ZF/8UohNf/20cwuGFKHuQRjZCAAQYWnEyy9wXIeUv+sMbZ62k9oEXUhNXWTBEwUBVb1Vs8uTeYmIiys9hqon0ZmqdOpP5rbKWcPhGGKX2ithoHJMIaGk8uwl/Hwsd/4hUdWHad/8//gwiDf9BQeUVKxfXJjcrjTMiNTcQUpM54skaCBQJgZdEk+EGqhV65bfJSXy/psQBAAAAAVKjYkIYIYFGmw+XRaSBtocnnTsXkDjKhZMmNPNYVC0FAG9pgmPaEYC0QEKUeGIWwCzBGwPCOdYy0JQzTccpkBYIUX5lik9RhfjlPs1E47/+7Rk8AYET05Vaw9DcH6sCt1hJcQQYR9RrJTcgi4wKnWHlqigNw9KCZU6XdTpsbrfGdMcX//yXgqlkeafQdf///+n///+pf1dkQn/y6a1+jX+8YLCd6FMQCOOdYAAAAAAqFacqbLWgU5CSnCy8hg1YIIqBkiAESanAy6cdSPM0aD2PMCQDuVbikafmOt2eCCxQcJZvxNe/MzE00mbWjC705M373+XJj2H43Gwmf7UVTkmn/+VCQVB+GTjf/zhLaQx7/ddxUdccSw52JZ7xCVd0McpR/g/HsODcCExuz+/6KFBISCF79v33IAEAAAAXidVB53GZbLHih4SfFEU5gREbklQUKcFTdUa53YZe8rvRBOUio5igIkJBCpiixValba7PQQsM/uEttSpGVQaEx7j8gEw/TDkJZ8XTIXpEiJQ8oeqqbVO/M/I/HxnCTmx1ZfKLf/9f////+pZfege/qW/o37+7GJ/Wky4+EQ3JqCaSzV0ygUaMgAFHCvYhBfkdIEZjK+GAepiIDYIL+AQsiWVA1hmk4VoBWeFmAqA5JVFo9Wo+oosDAPVdvioS04RTkl2c5R4olPrbHn/qk65WFHwof9uLQDSRoV//0gTAQsaZ/8MNvqvlHF///0P5l0zjgSPoLMIli0RJuti1hcN8Bp//qTTKAk85gTobu+z3UU7DTHQQBNRDdGYuEWZVlfFXj7o9EwF/EiNpxJke7xQgaQcAubArThJoxqdghppfQ1N4iP12+gxGVRK1CISBW3isWD/+7Rk8oZkaUxVawtOsIxsCs1hjcQPtRlTzL0NwgSwK32HljDvJqlZ7qxDdwo0sn3/jocqgIij3//9v////70ndFe3nHunfJXbIyPz6gcaCHCAJkDxhIQqNAAAAAAAFDIcMlYwTFRA8BHS5zwCbpix5KACwZqJykAIDJUxaD33lz607NhgAPCBqQXUh53ZEgdAC8mQiRViyzmBo3RbcQctl8OL6ZvGJZWvUev1C0wX7g6KQqt3xEAQIooAJYqv8eYbCkSzR0n8ia1DGKuODou/yapeppSFS5oJkOh0T6MB0yhYMSXYm/2luf//UpOnLdY3cgIAAAAAQKpphu0v1mzKmDWDO1LISqYyquRaCZoTWkIVl72tL6RWd1rLW3DCCgACq5d2CS2DvI9InKY2y0udoGmLqfLEWA1CEEyhsKFtJkoAdKLLEHS6SquNFlgQmNXqRFn1usWHPS83qYEBC7//+3/////ZSFYr/2l5XS/fRTP+oqOCAKKgI5bjhAjwBRIcW0DmRUcFKJTJDNbI8EDGwShWciGSMWZSJ2tYZU7NevTPEgAbqXxtRqkYjblaerpu9LZa/2/giu9jBlFVKKCna85XfqaEgVA5Rc+Kxs48ob96vFZUNHCVPJfyUsO0NzP8m9PYZ1Yn0ydSJChRN36RadtAyLHmLeUGGJZ3X+iUAAGyQqBBNVvq76R0AqUHDPo1jxVYzCdDRf7RA2ZYGzhQW2zdN9GEDqTrZa27HCwhMFWByL8dJuMAfAcR/GSeQp7/+7Rk9AZkxkzTY0dPIIwsCq1h5bYQJRtTrJ06whmwKnGHlqCtJWERChnKjWQ9ywJpQmSXNhkLuhpTqdnN1WI1kdtlYG5ZZvUJggg9H/T//////85GdXVm/qbubWv9tH7oQXGnM8YOYbW9AAgAAABEyBZQKmLjYqqqPJO2cY63CysRauicKAqLrLV4tQvSehrJCAl4+gaw5nK5x5uwALbwxjEKtz32IvbOTkzh0qk6N//+SZohEtp/yxJvNov/4QydnSUErbTVn/WpzRO6ueSsff9+/009xPGbjsSUUWIFTzBtt8uhq2FXiZ6Ba5TdG+upqkPCGn9WpAAAAAAA4DGATGDdVXssctRM1HzAOjIJLCBQgdoSTyjomuIQy5/VKIcFg2Ws8QShG7goplmkVy6JAuGDggdOmXvg0tJF3WigYJ/oxPhzbB4CjMCuCla6KVMmBIZIJoP9HBzGSUhpnCXlkK9ydPrNXr6jwFxxJR/yrP//////9XojJ9L7/rvyr37cjKhogD47HjRetU5CBIASLpYgvRiiExualCSpiYXrLysftMHZqWZDPRlYUdP4ui0cC3IOo4ecqxLDIMZBISXDH/fSogTIzoKG4if+QLMo4IK9Spcf/+l1KnBoq8tvj3odXx0Mj+Ir5atb74GiCLiWAbC9FiIsUNqLuRuTKxkZZR6fsXOAAgFUy2SNhVPdddopNZlYgcqmh0RuulppAlWgJYm4CSBTjUNME8QM0xLlxHK9KsgwNFVHWXFRGAhBcm//+7Rk64JkbUxU6y9L4JSMCm1l59IPCSFZrD0NgfgwKvWHniiOjlKG0XRuYcItmXKqTyKYrrTCxPJ3Q+BMJyRA1T8qnjgKWMHC+hzSrf//////u67277bdF/oVM+/KD5cYF5bpKqqZYDISAAAAVj2A0Z7gt6aS6mpkNwkUBHQXrSCypYcKAYo3GHI3KLHYDXTJZc16l7II3GnAeWSYHKf8TI7BIO0tiH/8OUVJpnXlSqL1///3mJcQ7rc9/w11/fzZgcbnh2+9i5ovC9fwFhB4KIOoGIQ+M11tgxOtR3smCZ1dbKf6agAAAABAzaDiL6bWBYkDoFwmhUFRE9xIoQgmeAQmGoYZYhIEkWDmywIgYhmCkxDDM8MJEYoYM0JCoAIEF/CYmBACKjgK8MqJQBPO5UWfZtg4CNEnblVM3B0Ff2GsqDQE1pxoaRtTIVzLVHWJMAeZcb6yKtY/Cmvf+cCnysxL9gLOXn//+ZGoNCeos8Bed3eKNAOfEzwYCAAIAAACS6AIzCYLYgE5MYFEp2mmEhzTQadBy8BYMUAJsIs57fSdiANUmDEMJJRk+fRY06cYLkYqNLk5b/+EUYKbVVEjMz/9Fo2GTtlZov5S8NW9Z/jP+aU6Cmff+3/lu39PmP99f8i571OlwUqUwcZYlS9Z5f5SkFOLCwbKDEPv7PigtNMIEIAAPqchiG30fFMplms8XTUGRAQ1RBUHDgUOaxVD0JJKilYUGcZdlGQkyASKLBNAaJIgrg2kwdDMTgkT2C7/+7Rk7QAj+krX+ys1wJPl+mRnRpoQ0R9X7LzNwg2wK32Xnfj8WhlsFNeOxKaFGNdK9iosParDerH7M5ybk18Z18fGRsVF5/Q1qt/v/////t610Vnn6+3szTG+u6BKEIIIJT2MEQsRzIAAAAAAWOql32cI4SNMNRU+BUdwEkUFt2LzAhACCIDVg39fxIxGGCEPH+TMLXKUMEqUsOrwYO1kzgn7Jo0k+m/9D9AeCqEBnP9+pM+6GJJWJ0cz5V78MBoinKIgajYkb4y0KUQzL/+6df+CmHr8f63JQ0qhrHi4eB6EoKc00Z2hKOYExZY+j5jq+B9Jic1dmbVQAAAAAAADJ4y0O6XYgClWFkpCBLczAFkr1LxpLg1LBn1XsvIVCs9W1ocuVQWspgiEXDQfUiiC+MJTpjRdRxs7tPR/DhDdOg74mmxJnOfSdSCQVLGd68hCWV6PRJmGhO4v2bX9f8wZH5E///rZ/////1RUJHJvdWzlp5ny05ytdFcfYVD43YJCuc55FkhgAxIQBN7KzixACJFJVJOB0Q98bMIm5NbIQMiLkiyq8/T+NQ830iFilkhPxNdTStzMfIsaGqhXQdf/D4dyE43FfvfyeSJJdD/YcU3k18p/B4iUO1T/xuy/rcbt8V/Ksq3EorOEAjgPlFJY/h52EWhe5uILBlz2lnPt/WkGAAQF5sme3NFnjdFgGfg07TUNGUoIVkqUOUxNoaGI8tij+sEhK2TOZTVVRmSuFrOI8any+zvNNly7oMlFSpj/+7Rk7IJkiEzUYy9FoI0MCr9h57YPbSld7D0Ngf6v6z2Dm6BJS+jzU3KeOS59WLQiH35lmEzDzsuvFiJYqBNlIy3zJRjzEU/9///////9FNT//1Z/ny6TH7z82cD6UREvvnSqQAACjoCMqpLHU6AIoSEH2wCwgAvg6ajqFFBqVhpXoXDudLUzi26ZDMy8ZCDMYsMGDFjkslKUsPzYUDJOHQErYWajq/kCROL4aFQZijoCANcqINKdwrPUEdMSIhw40oZtOX0vb1tjyorW6d3r9qJScMRRasr//+vt32sx579TL9S3PqNtjJVyiZAXI1BCuFkZjoPUGpiVloy+RemAAAAAAAAcH3yMPAyxchmCE9hRnAW9AtUcFgS544E3MAoG3aWXNaZDqykWahdtnYAKxVwBGKLw9GX8IEyolx4ktCdLpVcTFCHGHSf8ypPZmOMNFsRcNgYUAM+KNZDU+qFcYTlPO3f5j02eYEgcKkOa/o/3b/////2zysjb//or+9BgchQyQk7zxmLI2FSJLyB8tQABAAghOQLkQYo62yCB7Tn1KgQ8QkLDbSzyQTXLtvPCVU1OoFh2laYkwXzYrlx/G4WGbJ6iyzEsl2D6PptQeLmYLoS8dGmdud/hyTR0AHj2YrZszTM5H1K/R2m5QO4MT7alC/hh18++O/TrrpvwaXE/wbppHEGWYHdntOybmiVmGRplAgEAAFk+IQgDMta5B8MvYYAs7T9VyyahCRpbI8Intu7QcNBPL0W3bfQvA+r/+7Rk7gIkzkdSK09OpJKryq9h6rZQRR1RjL12Qfov6z2HnqDwRcUKJK5CCFuOxA4gD4Nc74Sfyr0+OJshq6JiMtM1kdaRQTpKE0xXxgGhG3Ev/LXdyqDgFDk0f0P/7f////3zVt//6+vvSbjmql46JxEzomaacAACAAAACSfMGAyEzFWRSJQzFWfEKxNFUkkz6bhgNqUJ1rTsy1rkZ1KmmuGzOZzwWxH6VO9wB4yO7xt0UxJ88n1ZE/8M43Ldv+DEsNjcrU/byRHMOo/xPKg7A2//+Lc23cdt5Rk+j/6Vfq54k2qOkaM7iTaKGW6d0OqNmsP/7qT6WVxdAAgAAAAAnk7egARfl0ElwsegRjUxSnYRDbwqPLjfxr6Y5ciLqf7FPkQljOYzjUCeP9BBKDdftTMN5LGy6V8BhRD62KW3Zkiw1mlGJ85ODiJiQDgLFY4Z0ZCYrKgPINM/lP+lk////+yF//9vTzf/Qd1XPUMkNBu0+BAAAAEk8JjyhOZN6ZYgYdM3A2CuQoftZWsyecAwpzS3K9HCayvpXzI0bEXzHAO/RLnmFB34eFYjSqlrWMBSfJ+1XOY02f+Gey76CIESAYJITjvqVKDQWhh5ELhiUGAhGK/6ETt0U8gRDNuY7ZUPSi5MiLIBC5ET5VdARt4MMETpwmW6FrsO9znSa8nDE4QnMMpW2AANEyjw1SgYcR7Tkj64kAjiSColOQ71QgDfVPZQJ311MrUxSYXwulZDjMQa6DjmnuUoSrcu6HHjMfD/+7Rk5YJkHUbV+ytOsHkL+u9h53wSVUFRrSk6whGv6v2WHtgbqTlFLgAYlmV2C+6IRyhEgnjodpWQ6XiGfLoVKHLquZQto+aPjQCxqX/r/r/////vRDG9a5pPuqSN0a/s1HHtZojCO7jVjKjlmYAAAAQAADhKCZYCD4CXeMvYzE/1IaAoqzQcC1Am0CwCrU9UCbwwRGHhggwQCYov7YwnmWS5yGUvkDBB5Fll6/++SBmyBsNuVTv3XkMh/DgXQ0CgBp/j04enCr8ZEhEUC5mHv+j/Q88u83Tscue7xaIiTA+S9JSnLznNAuSBUGEih0Gg6oO0klvdqda6p5gAAAAAAYOp2Q8lRQYM7gswhcUvKXbEJFrC7zGW8DIQhwi+b7ocCyrOFwlGhZSwZc4VCcq8QsjhgIezotVJ5Vxl2oDTIE2Icda8i0KS4xDCZSROEB8XE8FGpJ1KoScO2RnZM/f8EKOJAAoyX/+qe/////5XQWFK1Yzam1XKit/1zLZTiQ5hpB80cIMqwAIEvovlBNsIsTUvFgKwIDKJkF5WCvoFQSA0OSv7pFJkbaunVLkt2SWgjX3HUgpyZYnYFwa2colj39SR1CUM6qRjQXCkGPfx6WKgUQQjPxaFggBtEE/xUFoG8NicRRYv+/1K1JiVP5D3CVaHrbEIiXTZwzee/U0tiOq26n/FF/9nqeTMhYb465PVYZHOnolmhURFWIER11uuoOl3FkdkAZchSUQcIac76pm3SKbisybRQpSiFwDVHxr/+7Rk6YRkbEfU6ypOsIusCq1h5agQVSNTjSk6wfsvq32HnplW4Znl46uHAS0mjfCYk/MwoltT0ByuoWqEzMomhCBoDFERUU4/JGgaDCY3c7///////+xynIZT///T/6bD7hMNBkH5dR1xUOUwIAAAAEFHJLeIIUkHdMEKQqO2tJkRhB7Hiyg4GW2a4mAAMzWKxaXI5R5fKagUAUXz3BTatihb/v0bHwhqdXL/+CmhCEIUYDsvh1y305//8NPI9klpIp//9CKgLNBM//JjlmxCkw5TfsP4f/1lo6TQDcmoXn6TGeszZQmqVG8hJzdv+IFE2iZcwgk7WbTKtR//h0wAAAAAAAhGxJGOPsGxdKWlpUMQIRFtJFFdP0BmBagEBb6wgiCajhVaMxCMv2H1QjSrWUAhKnhtiSBMuOB6O8yNUkAyF45KwYDfLcA67/Uz/tFWI/B95LJRMHMwGA4BWO5OOCcDgxH03Ek0mJD6Z4sEgmDx////////9dDq/Tf+m/8y+70YsOFQiIhELjiAvHBU61gAQez5BCz3AkDIRoNnAhExlWORIci0irAZ0OUypK+ej8hlIKEh3H2g6G/qSibGhvqRLETERYvh3/1K1pKHF4w4TozLNnj5/48CwbBBGBN/4IjoBs1vylDeoi9Q+VIm7T/n/+a1pdBpcNQ/hvNSdKD5USCweSwrRMGCBfGoTXJ6jTQ+1b/5U13///Er8YATA3DHA+ISBUaxorsQ4M4OAiiEEmOMjClNoW0WQv6iVgn/+7Rk6gZkkkhT01hLcJLMCo1hh9IRdTNPTWFrwd8v67z0l0hW0TwiCDlwJ4pWNuF1PgVwW9SPYKebNPXElhjF0Z/TLMkh1GRJKJQsWdaJgZJILTq/4/icgCi4F/////////lb/isY6tRHb+g7lpVY4QFBcEH5xUCKnIkAAAAATUF8sgxURDs7S1dQAziySVI8Mw+Ag7AdBKD3/l7d5h26ravK+0nvayf+Svtg/aEl+iLk150qCMxshRLx1Ijj3OJE6OmcP/Lmh9WJIQNGYKKppS9xuHmnl9dBoqz7ae/145b/BeLSuDxVphnZ5Ueo3BWQ0078OoRbSoAIAAAAAEBeylEdMJAJOM0kg0FDiyJr7fVgwQIhBLWEfASE8Y9hfNoIQmZamu/QRolaZqqCNj1KhKsjc8hP2scaGjdeeqlarOKxC8BIdXlLDiSNbWj4M1oc/+/yqmEJCOyQ9///////////7TUIf9C3dmOVCpEIIA08fHVJBexhAIhEEDgSw0wUMV+DQQGgRUmmXGFAoVCk+xAIEyMZ+LDyEFBoaDlQKRL8teakwUOAggNgu9JUPIi8oiBC3JhpcGGbdVcTn/9LTCIOS2LN26WDaZzeVG4OcvACSkkl6wpDRbfygzZLA6WnPP4WvPHe+5U28rlLPn/8+4uUxIVizxQPgICfUUE4p1JRmV4tMow7/yzsvkgAABq0wdBSMed4oDa+JjNSCyzPRCGAnwgw1mhJgO3BipYDRTTeXq6C/o6JBkAiVKXgGQL/+7Rk44Zj7UhV6zBNsoBL+t9h6n4SnTFJbbU6QhYvajWXl0ncIju4/407Wl7TYuhW/DHIajo0I+AkV377S2PR4XphRCfuSIT91s6GFrQsM9YPBxpf+8b9gU4EPio4f////////+////8xfQjNVAGcPAQdgMlqpIAAGC+xMWeZFFAinTSmevgQKhxEi60gCDFDBi2wsSGAresKUvYM4acwjAgkENB3fpY2nvD0jQFrYDhAADS+N3v/84wgmSaSIp+x2FWfxeFAcE0XCf+SDT/GZxCHxPFZtz//Kv576q1mthdbUZfz6vpKHOsGUyVhGBWoy5r+O3HIo5P/regAAAAAAIC8AslfdulZ0HtGwUqARqybrGFxwYPhStZsm+lAiq/MZoEiybbDF+KoqmWFb50k+FM6teB2tTMxUldRMptm1itrb1wPA/kgoCI9A4Ax3UNgmFsnraHl92aTI4OFTCB1H/////////nf/9P+gz5x5Y9bFTRAEbYiv4ABhIYXUDCwJAQFihUCHt6IPmXFo/I3gEiLFDN1igaYtSmkuRAFLXhR0LdmWSHtwtph8rXQ15i7ISbA2Ix5YhU5/7f9uxcY3kDgzsiglSdJ/bjuJgqtctIh7s/zQaSWLF5f//oSI0SCpZc9I3//CUW98fSpyGrQZ/j/XrZNkqGwbBYZExUmJQETJsivPJzdabznP8zqAAYwQLIPvFqRPxbBynpXmsImQyMsCUQgnOBA2jDZHE1g6MJTQVtU1BSzAgvepJaQimP/+7Rk5QZkJkfTw0pOkH3r6s1hh9ISkR1LDWEzAjIvqiWcHfojTnZIYghigdJrUYuvWuls0hpE5lDG3wllLDscQOcqnfRB1SF1w7ECxiPTTXm4uDO1a8Slv91yaJjgpGR9+3////////yzf//9+JhnmCwRGJGDg4QhYsNMfIWkAABAIyGCIdu65EygMGoEfWZfxNIeLfMywww82UBYRHJRBnUO2JiEPuhLh6LQDPtiprVLDrSEcnzlv9/OEw0MiwCvdicASm86/eB3FgD0yAbPeqP5wntaYl//7qOo8/SRu3/9x83ty9xYaMXrN/nbtlllrN0s9MfSNd3vPqnRABPiTlntAgAAAAAABQD7tL1T4ZdyWyktZClYowo8kQqQRPVBDxShFTAGY4nGuxNQPKPPEGybIwyWOSvHauV5VszavvU/KX9PraWVGYLQdDHVHJh7RGvGKMzmEyIjlXQhd1ocw6PX5/////////1//9fVOc/dzTaOULRQBIjsWwACJgoMT7SKa2VAh0DhzIskLJCPgIMEOpiIooeEKrAF6JVvDaYwaTjI012nMvW0hmtJlFJsgMOKAR1lWMP+PpfQWFzBhS5TzJrtAX84X/t3oeYzAcQv85BIDYRGi9ggPn+V1C0nrtLmope1elav5YdghjkbNX9+ykXapSXriOZCOXj+IhPHg1Om5rRcytUud3/6va6QCAAAK9NkxUqWnYYnB5mpsyX/eCpquRgEwYyyT4IdwuU969QaGFBE7BgwwgEuntr/+7Rk4QREI0fUyys2kHlr6u9h524SdS9KreFvgjgwKnWXnqBFahDwzUqBkEBH8YabLuNxlO3YR8eIDiLiT1inX2UFuPJeIQXww+LIX1EK1XNyXLcnmLDSuP/umEOY8k6rO///////+ex3G3+rq3RX6m/5rTUMJlBaeBwXPmCpTwfqmQBAAAAS40sWNU0C4LsDxMUJ+WHqqwGkm6JiMhRNdiFdmV3NU7cmXP8RESLsUblAO27NdU4eDXcv7djUpZBJ2byTcckk79RCMoJQN2UakTqnC/+XLnFiQjoym6NXzFPQkv+NPfs6Bk8IJkBRqUEf/VNwzSe6xRE8ZWelIdQFBAAAAAwPcPkGkSqGpyOToMh0SROgqFYCyL2IkBhHWxnkeCwWFJECD9UKGHcCoNZXkEYkPRsrjHULOq3mCUL61D+13i7C6M/HqETMGTR8dIYyyG//8w8oGcRDY5v///////2RSRzWWtshD3OKWVin//oTzGoHkUemAyAQAAALW92rAOhkseFhYSFz/hu7JFaXkI3jXkh+7sKcVfWNSwYqYMNV4Y3rzb2AXpt/w4UhxoqRWkKYKQGzX+W7cGJGz//+8lFsL8wOf1Hf5sVCIvUOaP/muj/+Vobf//lGkcVUOK0eIksIQ9xqtbsSKA1cPQgd18fndALkD93/ixAAAAAAAAHxK+osNwgECNrCw4BKqmRRdIu8iAXLQkANSN5c5eCv0D13Ftl8r/DPplxUhMInCwYYepFh2hZc44k/SMxa65v/+7Rk3wAD2kdV4yc2sHlL6w89JdJQXSlf7D0Pyjcv6v2El0i3fctq0G2MGR2GnnRGIBGF0CYPCUSMTFCw4KQtpX+278IC4TBxJBcV//7f////94HGOHVek0yNLxNEldL2OhL/caZ0lK848tWgAAALHGhiBogCCMU1QDB2dn+fF4UeFFQQNTSDBZnFI0qHWnOo5M78fTBQkEIkalGHZKgY/lDZaFnaqkQswZAcaemmcM1AXE/kYYXYa3K79KiAFgexGogQ7ym/PYKrj+v6zb4XJpZXnv+uIftaqiYEVn//8dQtOmNxOGkeyW3VcldqjvcwwOXJIjWnrqp7OJsUnt/nMsKAAAAAAAA0OiNYYgt4RFxFAtue/JeLWkxdpiRekQcUKc9e7N2HX23h1259BtOF0mYtHWItdF541iFrGzJI3bEc6hQoWhAr6bNZuPRSRyTGeoTuVziwHMjlX8MTkh7iyxYsT5x/ClAQ0if/9U/////9HIaf+uJLQxWXRmzOtv0Vim6iI17WESAA2p0u0FhUAv0nWLCS44WQwZdqmzkrYgpVRC5dvzEcqcrzEBvi+EC07VY1ySqdM1X7nu5FrtWAowvabhb/fnhAHcBA3ElDBOds8qXUl7o04J4jlyg3boTRSynxABTkL/ySDnebEgQaCBYKYuqixA+AaoH0uUYP5qFspe/yC0qQELBnMzQAmSMtpWtRg5DTvZal+2J634EAh5JdRk0Op/xmJ0tMoAst2GVIxDsTJNQ4h0FOZLtVyvH/+7Rk6gJkpU3Tw1hbZoUr+r9h5bYQDVVZrJy6geQva32HlqHjOlLjiUTi6hv4ajJ9FsSCG45hnstxs3knwq2yPbX831CQdIHTIX////////u9H/+j5lborakSb9YgJidJREsqpBAAABMQQs3chGJACXQjpsrTXx4uowmCuk0I4KuCJwLOymZStcGIMkXc1e0zp8nUFRJ92XZJSpVCEK14tUu6aO196hybEWKMOpY+9lvXbkNK3PBKorEd80Bg/EocS9f4hTjS5pmR/4ousRhvAtLE///59JT/Y4RoEcOpgYg+Buw1rKFx4cT///ELqKGTcdAIAAAAABEIBj8RKNv8guz45YYuCOAUVX8DgZhhYJJmyFBjgYIAw2AqSVzsgaaGiRh1u1wwEMVzZEmMnCthAmz4fXPxBtSITSlxKzLmFXoJAcFOifWxDabbD35ja8i8zuRCJqPQpHNdq07DsrAsudiWQbT9oca94iAcMGCav////////qJt//ouxf+oZ/8KUY/oKzAAE4hPDk4JGmBAq3Dw1YwrHQ+R4T7WQIwaYJYQNNVWaE/tdYjtJd1S8nyqlhocBJmZw2nwoM0qkd+lf+/HX8koMAJQODF47g5sPfQiIBuAIE4l5FqMRIHfs8qVyymkHQ5CiKVlC6lB3KfzVbY7HEjNED7RH3toNdHLOQSCHeiXOr2AAAAqHZYsVVrj7oXQfYyweGS5WSW6FAArSBgAFcmApvDyl6iBlAVS17eqqs4cEGKBYN1FVFyx9ij/+7Rk7gZka0/Ty1hDcJOL+n1rBYwQNR1TjSjawe2uarWXltisNEeRNEAiQ0T0XilXSsjth1kFKRxNleUCYO8vBdiTNLNIuUYxK9ui6iR/HzotB15P6f/////////93/8v/3UBXyOgAAACHCIkIWmgFKoJqbRTU+AgMNBSYK0t/BZGAjQKoIqN0lzwp0poiQlrxfdmmcsbEXlLKs2UxYOlEga55ECc+gn8Ue1iGBHIYlu0rGryxwHy/tIstazpuu02G+/9xQJImFxT9UEIVcwiij/nKi01KDSePKV/MStL5RIkiAShxZMdyRAwoHIm8mUkbvodEUYAAAAAAAANIQg02d5jFPGVoHXEo0vaWBRQZSpDjhiHYlPBSJEsooAtBkjEoQFHrAAkFEmICneYzRrzQCMgBVVTd9Fy2kH2cRVlj2KSpUJxZdKJTWPfA68YfbE3dn7hQtsSWyKi+px+7K4YBcOD4Zt2KOtqc7oZPGxFS1f6t//////////msdM8qTUz9an5wUeUUIU7cmEqXMEVTXkf35EMVDGTrAqAgE5OcicXq2ZUkstbZzBqNbx1mlO6mWr1vlalJiE9BOhA+FbizWgjvF1CPCqOqVhlh5sVCiJwLC8HgCq/yINrzFb//NWGRmYU9rL/llfPWlHt6vvl7qhtOqTQakh90qNCbL+CiNSK0l/EPiABAAYE8DjR3iff4+wMzIWjBanE88iVKaqp1wuOj+7UfkMkZgqo6j8yaDBwAGCzSmis5aeXDwFBwOr/+7Rk7QckeUfTQ0c3IJHrmn1rJ34PzR9RDL12QdQua3WGKtAUSVTRp7W2UpbfHgOS3zwniCWbLh6TAyOOqmnU8oVHpGSId/X//////////sQP01YjISf6zjMXlx5EKjwAAAASB4QcAkJDiBGsaKTAA05lSQWLtAosphECDIIY6ZyYFfoWv4xWezSTV2DxmcsYYCQkitIsXUXZDZgFkISuAQDCN/HVPKpJOjj6nLWJQtSTPu9+TGmXQFAKt6fDu2f+S+Cw4vClQ2imfvi4yOFh0tiW3jmZreKcrToG5cUW+37aUKj31is4taZXmThcLJTeLdIK2Tr7xav3n/EdC3hAAAAAAAAAC+iQQKICMY3WmfI2dUiBmRThUMnkYoOLBDSDDCiDmDR1MOxjhhWAIRFLQMIJZDKoYSZ5gBGLmhpCXJpCg6lCacBbCwCILJQ0yJG5wWWJ3pHizEVakw12WRFqJAh2YUtJnEhmX1VkgWKzsMpLq9kXY7MvJzU/rx0Ix0Rgfmt+Zf/////////j96fsj8vt/5pYijI28gB3AoQQQkgilsFUDFzgC14IUODuSCggQmxoOPD2VCztGriSDnAxnu56J6iSKinOUY+h0wCfz/+rx8H7VSyKMw4DviAUgCgvKE3+NFid4EOvG340VEYmD+b/+d1bgaSQHf//D7ds625YfjRZCZIVJOc+ihBPIsU//8YD0etwAAAHk50DDACTeEkB6yPiB5nyZ6kYfWBa2BIAuEqUsmSqRBK9ylU5Ixv/+7Rk8IZk/UfSI3ljcJorql5rJ35PlTFVjT0PQgKvav2Xltlpzyq7SpM59CGccJ/0TGvv3Awl9MR0WwE+LuS1mjPk4p3qELKoVY7aqUmy/FjwmJEoXJrKsz/WNzHKIoIN+kv/////////Ed+VuvUOMKN/4QHIg4aKjIhQJiAAAABOvcs0sgGmMAldIzTY+pn6kVjUbcFXqLq/l86+lfH6aKuJfgT8nQFzFiYGB637/0mR8Nlj9rYpvXXaNo13f/ljT4iP1f8PBDFhl8/zG1LRM0QcWLXcur+3evvGKBXPHsh+sD+R1jyw2DQTDuBu/wP3g+ha813gAAAAABsEBpWTb6KAIXLYIM0lIBYnBCM6RApYQgKRMiC6xqOcKjLzgJSxisC50Fx3YcyqEdikjD+PpQGqQltkIIk0mTwaiomixQzykokUubhlpwyTGUqmRyTTzeZyvnq5xvfF9y1o+f2dy3///bMIi1O2o3Wx/wPgsMVICAAAAAKDkRCAaFxWCTXS8XwTpFNFHGrMsSeMmFni4h6kcS+ZJV0m4FAQhoLPYpUHTO6/9KoMsPAkRfzn/+S7GIogtdgGfvUfO4eCVAIAKmiL/8HDJPv/Jt2EgTByKX/8vzPDTtJINMkt2XlIt7fi5xc6hQg8k9DT5OHmiOI7ANNa/WErc21ntwP6t2ABa+BYQ8b4NVkT3A2UAiyMqkVKCQGY0GYiAYoiGKlLyq2TopK/JboZlrSUz+rnZcYrEd0BztFZAqAOCqVYYtm5r7v/+7Rk4wBj201X+wlFMHslSqxnD2YRhTVTrWELyj+wKiWsHfhpKJp+F2oUL9s23+hpZlO1hua9YFl0PN9IbtLOwc3BnsDyvcM4fempy+eonDSnt////////3PNWNpmy1eeYyEDUS6LytX2/Z6pSUUdelpwNQAAAAESz2CxZQotFEvqnreGvp0o7ljHZVQg4BVG1qCsx8Py6QVDmvfJqNcfoucaxhX6Y3nw8jSSLg7XpKH1DAPJ//+Wvd/zGqVElYsNL/+fbGaHpN1UDR9bv+6hOpirqrIRM7ZsqdPXJ01WSXQU1DXbMxLqowOn9ESABGXajATAAAAAAQLywJGVAeTWpGe5hTacDQRYaicBs+ReA6U1E8VbEknGaWqkr9M1+H8XOw8lcstrsNF73+tIh5eHNaZpl0QjkMKW0NoJjk8E7QzcWipb98dOsHej0uxTabe0gOlUaV////////XHWPPH+k+c5E10JtqVvxOcQM9XoVEUXkwoVZZg6NRvMIBiAAEzqhYYEqloRC05Z7XTuOR1htar/tXReCrRak6U5PCmR9y3C6HYeaTd4Kk1e1gSRdFbAT8T/nqT8XYP5GRNSP3X8rtjVdj7af/6LB9vWlNkDxYRgai0UXf/m1E+TwaXUOl8+irpTqhASB4LDsk1PvHjBw9xCxG/PIuhbsi2tGm6JjK+YEACVMYRo0+kNM1fU72VtXUo8uWysOX1E+BYIQgEtXin/FkJLhQC5K/1M0ehlAoCamABKDZS2DKcWtxRUqH/+7Rk54Rj+k7Yew9aYIqsCt9hh7YQ0UlZ7L0Nwg4vqzWHlqGqAWQ4ktRr0h5YLs6POdRYMhAx0g7Y04b6KT28eb+FfmOJsKCbWf///////6IqGnT5qPU+qO7I3KKyvOgrxzirojPCZx+5QDIAAAAACa2NL1ObADAYBKPuAicLNCTFgjXV3Pi7K3BUtDjcn9icuq2nYd6MxiS0e1V89QapSgs+SAm/ys5Yjg3NqLX8FgsHpIfHf+yS0me3OIQgoLTAeUSP/9a2/ExsRw139R3z7iinElip+eItU5YnG7nTQtf81bcZR1qDrSWm6QDEAAAAAD53SROWUWBS/9/6xqGoInSgZdb/P8h1DlEw0HF2OsmAw1LK3AFtmSondTyVoXvJFA1sUcl4di4iPiwHqtaDJUdMuxniMqqWqrCwYvJFUfAiGTXjzbZgFBuOkDyE5//3//////fOVvm0yp3nUdfNQ140KVdjlQ1jjnkCBYkKAGBjESYY3IwYGBQhYsGdTEKgXWCgcHDGAioMZsAKADR6PRd1IhL6fRHEhAQLVEsG1KujiPA3jaKFCiyZ9gAlFmNfahFNDvAlg4x1ts/9tyF7FpOQfhdI///Xao6U0z77azOHjuaEEvnUG2fFv/8VfyMguGnvJEu90jhjmHiYDC8AAAUNUjM4HIEnDUFRYd/0F3wAghLEgwMpshRdcJhxuzheny/DP00lcBVWEKSsELAxJcAj6AWGwEITsVrclLZYgQmEU+KpmKUiyhAYkgvHKOD/+7Rk64ZkDk5W+0tFgINsCu9lh7QSPTVNjTy3AimwKnWnltgrzxK4n7Omx9krLAu3p0pwJCWr4pmVKK0YaIOtPuR/m4nVIbseyN/r9bFRMDlOLiv+n7f///////+Jt20ReodI2U9XKj/oHg6EwgoqAAAAIfLbVmUuGAwIFmABG1rgoup9Lpwg4UgIEb4e0l2VMAoAtCJMjAGgLaO4yzNrLIRQQqUTZYb5nj7JJEqna+Syd0HwCzVUEc37cS1UpOcm4fe1uixR0L5//8oh8IMSuIf4eS5YPp0+bAljuRuf/bO9SFUVrbv4v/bJWjCUZxN5W5c6VQruk9Tj3pa/5F1AAAAAAAUOKPoWL6QmQlQFow+YDlCjosHUVQAusOPzICwaYM+AMKZMGCLNLzCDaKhcFoiAlGdiwNShDZB0BCQuaHQrIdE6MssSvUx2j3cVkrjEOmI1m4GIihPxubZUcBsiHmPtgP1sDYMzUWJv78a9nULhZxa/+MX67////////5DyX/f39Bb/qiiipQGMgIABADloClR3BCMwy0kOpZ+fGDgccAQRKKhBkgPgUJ9RluMywCRnMfh2vvKTIvCzIdJGGk+XL6pItYFwTF6XY9P5NTo3IE6//4VOd/zWaKplRkbSffXz5s223FIq1GyJv97lJcfOwwayQRCabPTLpueTeB7hrvIdJgqQCcwfNVlLRkMMUkfHpl2xaiETCnRj6HFrq5n5eGCYXK1sR2aW/AFDSoMQ/Wiqt7cXWvLPCCITeC7/+7Rk6IBkekhTI1hb4IuMCo1p57YPVRFf7L1pgbewLD2EiuBIw6XQOJzqEyhD04tIkGRyQjIZS3//ephkP4f1v/3DKtj//////////t///Q7To+sgwaqQAAAAAEOlxm4uk+LASqAXGEhRHAuULCaSa2aAOIIQN6LSTITlb0v3FyqLHzFHV2t2+6hesIdeVOkHHB4yMzVExOZ0KYiA6iLSmEKmLDLuP+5D8X/xeKB2dsUTXs///pi8dLrr8yyCXTHxEhJQVMvQiknXo6FydbuZ/8cn3mlRZtCpab5INjp3Om8vceW4q/////1aeAAAAAAAHYcQKFC6TAgZ5iSVhzAQyRVRVXJRDSCsGFGosHISMWMOGLLFmE9FKYFMAJR2bRPYYKheUEDo4pfKRCSYcahogLriTIA9BnWBkgMa2nLWQoYyEraeIQJc7Ml4G+SKEiUs3MqVJ/GYc6+WuPz2QRwcmKM9bVNb//////6d///T///Rs58yVMHLQEM7MeAUNMAHGCZEAHg5heSf98iCOCJFEKhgeGfBoInc05NWKxJbgMsQKQWfKs+wzFXqzllL9ftAashRO9vk+6cvTcBGo62a9EpfGtft42uSpQNLrv//5oC4JmPPyO2EIWBWUuKjTft+RlZ8yUULGQKX/6x+1QSIwKTXJNhB5ECTHjyC18PjP9EsYCC4FKiI2CN9EHGkpNt+DxaeLgIbLBDwMZIjDUDL13JOiNPKGkKGo1IjkyiShNFDukmaVB4EeE0wuMtC8LX/+7Rk9IZkoFBTW3lbcIyMCo1p57YRLR1NDWEPgi6wKn2sFjAaZTpiCaUCPFUZmTQL9u/z31lDxuXH46/LO+Msg225eFZ9Zp2IGh+eu8/6uvAU4eAriKi3UzZn//////+jZP//b/6juj5sBQ18wu4WWqgAQAAADmGAAYoc6iPKAECBBDk9LuMaYnC2WjCYq6CvZY2BprsN2cp+SyJiBsSbWijZACgLawo4y92F/MBda3l3TVYiIkE4y81Wi/8d+Ao8lB/BAIR/825tlML/NMWSeRjxAn7/5rzh7OK0XQi6Ez1//3OO7sXTCjhIl+7HOMqyYA55GQ/65dgEAAAAAABtUSPAWhIEsCu9NVxjmKb9DN+UG1jFsCwmhG8bUQKFImEuCpFtmkpMKsW6scZTU1RxSKTSX6yBQMpIWpTNjPEEcTxsGvvLkiD5b1MSBLIar12j21LqAkFyoiBYeIKQ1aXc0VIQ//+jf////+ja//+3/19HzceJeOsOO8ECFKyKnLhlQCq92zyxlVQwYCgqW4FIDgAwbMaoiyTDQlMGh5sstInF5lOHBgmXLAIJmVuUoAB2qqytwII5/xGPEW1ju6mG83P/L9IfPtaU5Az5mfsfAJAgJFAbkB2nq5LE1jE1MEh+N//1/TbzJ+mulCf//TYZHkNcbRrgmj4YMIeXJp0RU5a+oODO/j6HggIga8IgTbJFCkvLkOxU2d19s9GQVFlASQIgLA26YQ6WZSoY4GKJ/M5aLAoKYV0mKvMGto0oPR7/+7Rk54ZkMkhUYys2sIFsCr9l57QR3R1NDWFtwiIvar2XltiMF94bUSVQgXBdKF6hw9Qt5Up7ypN6yqHIOw0l3HEYZkAuW2qTIdIf0G8WL/l5UZCAuIOV///F//////Vtv/+ejHT4mMHPEXR81QKPGj6BSXAAAABuo8gbUOBJkLOyPcvGgpflVcDCQYBHAghkgES/7hqxOdMSlB0lBsYykr5tmCxBm7sMJQDprLuf1NBXN//urXCpFJSPsyf3v/l/z8ZL2L0Tpm23ovgBhLFwrC4x0IjjDhIHo8UH2+8fTzJpaq6fEdsTP5xNgot10FI2Yb+RR17JrAvcjH0XQEAAAAAEZ+Gw55VZH+0X/XOYlBc6EshS+jyjJkCIEy/aXaPgsYWAWHFyphX6mrzMUeIcHM0Sic9VSGIDmmLv81mBr9aMNbjzpwLzbovuj22tmNQdDkXUOYQ1l5qsjAuD5GxN7/4MxLUgul/6i/83/////X//ydqsyNoQRCQdwp3bI8CDQgPx7o+gQTNCwA1ApaVDVxGAezQBpF94DgiROSW5AQZrkjJyXCMw6V4tiG5rOgxPlhx4ho6WadfV2/0zDUIBGO5Kxt//94iD4Wy/Pr66kcjNbz3oQJEDrfqTGP0IbKTKPs7HrNYw0fLlTz4+RYuONcfKAiJYnB47/rk6n0PqggOKcdSj2YCBxZ9OWRCs1FU1GbqHR5PZLQIFIUZgxQ3EQTs6EGYI7iTmaPkBkA5RnoLPqxSzQVU+cEm4qgLckjn/+7Rk5gZkQ0dTw0c3IIkr6r1lJeAPBTVZrLztweowK72HnfD/Bam1Vrp4lF0rzPbHCC9cIhwOSYr0mqVcblh4fHH/lU/Vv/////M6//f/V+TnHeONj5mFWfNmDlUwAAAClREKpzkQKgLBwGhSRmqL4XCWmKpptAgEAoSfIwcq76+Isza6kevwOYge9BawgoELKbVvMvIwAC6LK0a1fUWUblLEnmMURbMdl8nv/ly6pc0xu6aTKVLb//Cs18ZvOU6cq0c3LZqPREn750zMwrUsz2rJ+DtbrmzOHGQKFTrvONlYfjLF+sokseMwPVLppZdj5C5UoAAAAAAAgTQQltmCoZag1DuDYDzCxFhyHAcAJ1DqwGnQheApZhhIYsXgpIRCEnV9KkTCLbq1hZsChAYrXuZggPDy7bSGvvQ01lLdmBuIMgFU2drDXvjryIgMM6u5kjsOq7r/O28T8EzgPHwLksdF+qwayRVQRtIL97//7i3//////zNgv/g/X37fzEa1YKl44GCdZMFFNQScveCo0E5cBVFuYPLWMjuwxmaQiEhR0eXLsvkq0Mh0HKLwxMUhpAMcft0QElejifn5nWXeoYB+RpKUupN//LppJCSRBsO/5HajbfvjfGCY4OSRepuW/5/Gv9QWgvdfxJdrOP0YQg2IJApS095KF0SLiASID5CenEBSBAMC/pQkiWKX8NQJdEQYBZ+sZZDK2pkBF5wYtaBHLm+Q9ffSIS+gYoWihm1LGnwuJd0QoqeeXAGB2r7/+7Rk8YZEtUdSw3ljcJMsGo1pIuIPaR1Z7L0PgcGwLD2EntB76xLRKKlQgeOPOpISCEcLj6r2WXQbkBYRJuzf///////1Nev//o/b/3NtHiLs1aRoPIqwEAAAAAHU3xo8pQX4gIFCkfTwMGKpEBw1mAQFRbARAFTxYqrCqR1HkiYKWemK2vguRuzRi5pMfGBgA4m+qnI3Bou3dvcFQmIEUZI0aGKSQS69/0yPbC0NXYt2P/5360E0jb52v/u9QWDUPgGFGjpGNf6G+Q9xu8Rd/8s8Ld5BhTNANhxkiOlCpq2KBMBRiGXCSvk8MhiKbzgAAAAAAAAKWgjiYUQX05BiNhu4hgAQ8fZKrWLOgEBJcxekeRmbCozC6lNofODgV8SYkqZIAERLQ8hOEA0YLUIHjy6aNUang4DeMdgKADQNAREn9hz9y9mb5sIdZIuutWtBKu1j3n0cKKSp3YaksN3v+nyuBgSRuJI2OEQgi////////VDUHCZ79DDJP+n/f1Mfv/djxlWlgMW08mSRjAQxK4gIQobsd4quSxdJRRWxyEXFNodXLSQmE7U0TBfR7oLisGOjKo5LlY4k23y6xz8ZTcXhAspjVvVHV/KjcGDAx/x0iW/RAhGSo0Eo5vzTqto5xGh36mVOthUBb4RCRUTMajFE7l9JI50t3+KRcgRAAgAACmu5VQzgOSKLa2+1GCiwQ3kRcWFw0whyW5rYjMaWfdZW/dbjzQC2Iu+uW7k3Z9ZD6w9a42wFhLez/UKHzlr/+7Rk9IYEwEvT01hD8JbMCn5rB34OtR9b7BzawdSwLH2EltgxJqYplFhkFjK7DPWz/HxGqIioFlX/v//////1MZHMEEa87W06KnRNL/+jPNkFhjD6vgCAAAAAcToyqBilNgM7GzAIQQnNgnukWnwKgiyReoKFJHFYlpeUkiN9HNvZeuZ83XgKPOtDV9UC8IZut41//1RX1xuO3rr8zs1u1F0LiMOICHv/kmZL9TFQ9CUCYFwl2Lra2ymigRoYaoTig/qSP///3Oz7UyjFmw8Bgy2tGK8G5SqmSTQqQuwUYjytEdrgAAAAAAQFAuSMiFamwBSlbaYpzzkIJoKNiDIYlMINJQhnho4EBRIwyNr40IdEACk+ldLCpCsNDjACBltE8NsP0QUH+xkzL4KUp1OY62aaPDXbJt4Y3zGMBKhcluTwH1WpQgqqkYh3oW8hs/1/5dKSkgHyjzv3Nv//////1VXNQ+37v//qUR/r0IVII9o5o2NG1sAKRtFFRckvIzxDsIwW5GHnThwUDNLUZUsGCC+yhrrMjdV4ptgsU26UWjD/uQ1/TwojIhONprLrd/T1VVkskbeGuapNfkkMKXS4FIn/M7ftmB4DURRakSvcetkffYwpzqg7/SueqmoxQUU5Q+meUW2VgDKOCwdGVBJJ9jav7J2D/VlwACU7SgpJCNDCMiAdrZTij2ofBSVBMKupMQ0jwFohqKCIE3VVMxfB1H6Zcu9IIqjkxaAyU0CwCWVFaYJYHNHnR21lMIhmr2X/+7Rk9YZkc0jVay1OoJIMCp1p6qgQNS1XrLUaShEvqv2XqtFosJkMZADrSr8tUSoGrQkB6EQUak5K+nqMhAoX/ZZ7t//////0VSI5TC3Ofare3vRe2js/WQsc5rDhpSrKQEAAEAAAF09MJIwKhAcFB6AIDcwUOnUDJB2Iq+QIOTHpprkaissuyRvovqgpnouWZY5Dy12HxO2TmheA3jg8aT+M2F4biDf+arf4ISQ4SghFaEGPGeqxqrioupCm0q/9KO1SXdsvMTRWNilQ2mK8qKFDpQ6iJ0J5W5s+FKn7ZhYFpT33AgYAAAAAAdNwUCEeaiq6aB2Z4rhX0gdNpvMMQmioJQgjW/YODaKy6A09Ljsu4zhlC1VuL6mWwo7qjfAtSdh5LZaSD6USaYttlwqIR4SBuMErAkOREJ8+TgKTHj/fM50zCw+PFRb9DOp2m//////yMZkYj9WnqfcOSHVHs/c5s3Il6UIwqHVzIQAAAIUGFQ2wsBYC/wYWlZjLq40E6db1NPWFCpQzQFIwoEF0lCJayJCtURgBSuJ5wrK0gUBnHKCGwCnto/rMMs/91dEJJX6Y7UoconstY/7kvYn+mOtCT///igSHQZ//AfBCULiCMNXn4ua3rhzNm5/6JR/FSrvPED1U9biUTTTUTcwFXmV49MgSAy3qBWIX8WlAAGCYqFQ6LVW5NTauTvHi+g8VVhTojYNEAhuTLDPoQKLOYEinCwQoKWoBgYQMYIKlCx1CgRs+zKFrmAoBihQFuE7/+7Rk8AJkI01X+ypNsIbsCt9lhbYSSSNPrSE8glouqjWslfklQnwyGjV+/gyIsKlmhU30FwVDEHOCyJlqYqHW60J2LrI4hKo9CGeXqOtGqP9c/yCI6Aoor/xj+i/////f0ZHHDRn55WmezuSqp+pV/MxmHsLsBye6iQAAAAFx3kIBY7LgCULhadFTLSbU+ux0nfKgGYFAJS7LY6utShtWzLMqbjbts1yliNrGJcMAH+glEhATiKFKMUFRtSYQIDRESfk15b/EMoPLOEOv+U2vgf2yQ+l/8jKNl7mnFXDrJJGqwju83zQOniMoyzAmBhs+Jl/R1TsQgAAAAIGVuqfNG5svcOAjuVJGLNySMXYiGVH0rAVCS+k29sCNTtuLFGDrlhgcMNGAwgSYLVyZHx+QXK6GKvStUt8Q9scRRRlPEO1YKE43rZGfKWZjrqHA3//wQUUBEQj+v//////f+LYVDaFaGPd8X6MSqCYQeUAzAADanAoyhwYACAFDjxYcPE1yIuN+8LBEK24kSZZMM4avqtIBQELUEYjC5an/AT/xlLoqiXoSR4W/Kh7A+SSUOVNIxrkvMR3qgGmv/5ORRn/5AGiIDYq//5QwNTrWkM9WOv/LOdMbcTlCdkJCU6hh9BxKOpQiYwXO/lVyBw07GfzlcAJZSRaJRilTLORQL2ixIuwSjVSCSwwF+HSqGLBF2wWAWG1Oh4WLGQiKQCxaPAHYgcTJKAgqKZShkKFr1hlYVBlpN9K6o0UX3YIFg3gdl/3/+7Rk5ARj50hXawpFsHcoyu1h4qgQjTFZ7C0WgjKXqZWsvbCHvADAC2i7jqJeS0QwFEIoPZVraoLidxIIC6RKFMUTXv38RbfwYMn//xueJ//9b8SNOhlOA5JSP+WY7AQGfghAAAAAbT0OiRZMSNRIChAUzU5RhIdJhJBBeGVdJvg9mE1CTlsnb2MDOmiWF1nMEvpe0KV55khZYihz/+eSEFKcj7FKKjfynYqdqQpy/8vbY9yW95o8OA4ANV1//CC0f5xEjwxa/8w7Oyu4+DRHsILIHh8DUbZWKbQNMqDJ//x/rZ8gYAAAAvUyVZT0yNW9cxl7aqiZYCBFREyglAkNEDFgUZTnFuTRNMYAQgFxQUCPBrABGwXcMskzvzEDcMwRQaCCygMUqVR5LV5eOjfoGSIDVNWWOQ16UqSf+CVLFHUzULU8UeVuJ2NkZrHIy0lvLGnVljv0j8PvR+KTjwD0NP/jQ3//////60OV6/zjv3R//M/msh8rURINCgIJB5XZixCzB4gYY2YBKlYUhG4qLszCw9rLdQQPRgYmxdTGdl1mozpVVRZIeMP8uxm8OMbHAQcLWZUge//zcNugMAnKZw6srt6i9jIwHUqE1Gct7HyYdNy86ZjWdTmp8qEQxxv1HzLnhi0UR97XX/594/Zv0MqcZpiAxUUevjAZACgh2Zc5+50sMGABElY0rsobRNZoQ3lUQEsJhAFBr+XwSDQisoIBD5oWEFJvpzp0OLDJNaCGYjHiNUYSeuMMgjmZBg//+7Rk74Z0H0zWay9DcJWLmmhrJ34RUSFV7TTagkEvqfmsHqEQCK8okZTtAA2BNdvYFIBIIEplK9PRQuk56wr3LkLEcFpKklynTMYrEIDT3hLfQqMTk/Wpp6j80uMADIJJL/f//////59DUeXt1/zl/7V67U2fWOnyVWowMwIAAAAyqdJUHFQHo5tqFgN+NzcErGjk9Yy3oCmbvN0/oUTxqHdaC0QURdhlF2L/Vvff9rcoyXHWX1yhy7atfCDBBBEf+MgupMPbvvkVPIOEIG//+7RNY6EnYdtx/YeXx6eRBCkkCSkP9D0scEDIIwi2FOf92zs/wZIAAAAIT7sAZUTWzTFwoOAFVeIqKrNzWCSvXCUCL7KqIovq46txUr1CDy5PCECvISpx0rbQsJoykjtRmTAKoOppRHhQzBTylzDjrh+W6s7Y9KiYHA2QUFiZ3eUU4ammt////////mmWScTO//q7/PnKy8wuzzXYKHK2g4o56gEAAAAAiF4OAQD/AYxBAlauo/nkwGEILsgQ+ElBBGENp9Ljgdujqw7K19CRKdztPw0l0mrMlnwaPIXuXLDP+kYLOBXFzJemjlV21Ilf1UkWzaDVe/yjCxaQ+OQTtjak+TRGPHX/8j/HV/KZVJ//C3F5vzFu4jWyFs5pwhlrh6HAVKEK1YR1J/tqkqyAAAAASmS55hYSGX4EhZ2YQ8JJmyEBgQ5gRI0CHJg0bQXC5FUAMVCH01hCQxEJJEijJBMw06RTIcEaRIWiqTBFQdb/+7Rk4wAjykdX+w9C8H6sCu1h54oRZSFVrL0WglWuqfGslfgS0nuplNLsYGsl/ExgEWmIg7exlEbaw5T+Ok3eD5XCFYV1pBwBQxMYGjz2UGMr39yzl5iDAiw//r//////8wcCAwhwQiflN+v77/S1Z4wTGFrCyrWACAAAHGJGC1H/LdMqSRgA95nlaVfNEUGaUiCCD1VWIKdXQwzAjSHObxBN6acbmwDfVaHs7dN5X6vLqYEyH+BpPOdRq5omBcJD8bI48eVNRqtEUNioCgpX9eb6rMY3/dPeYhjuNjo66OhkTlQ4q4MElXPpvglCmAEAAAAABcOlVMyyNM7ij7YHMWsxWxIuAWZuCOqJfJ9KPQ6u2mhpKB9ndLQvW6zTiAhUkwrlJVAHQhvG0XOTuMiDYOydN1xyOiDA8uqyXS0oPoWBdDAEiJkNL0XuUD9S//Vv5/////+rmMRERc9X/Mn71X//nc4zPQ6jERKa8QSAAAwqOilAxoGBgMPiQZSsxUZbKKbipjwKBBHBBRdHxm7B6kzLXIgov3Jpun0MtcmWPkjoD/KIwpWxsu/3YhuFxROKBKWpI9wf7UQFi0W/8weeeSo8sf5pQpSshGu/////NFEw//87pniXf/ts8qiufTzS7OpDrJhBmQ2FziT7xKH9v/oTF2Ao6Hhl8W4M+EQAmIQbxsyV02QMAwpFJxlTiERmqukvVIRq1AiC8MMRYVIk+0RUgk+Y0zNgLBJ1IyDJCL5oYjyDroqO5Qy+rTKoFNH/+7Rk5IJjsUhWYw87YH7MCt9lirQQ4R9TrWFrwgGwK32WHtgJxATLQZvLm3i8fRY5ac2dGoTjQauX/6t/T/////VzTjTSRyn/2dvP+/qY3qZaes3jo4Tq9ICAAAACeFyQMEJ3ixGXixJOgKU1eFUU76d6WyE8yRwmNLceiTz876wVIoNGYBftty8qo37V2q4uiwZxoJzk/zce2SClY2o01JGG2hmpUbikABQuM/kAfC1HH05QWD5UgKS31armK7qa5uursiHsuXP31CRGgtJi+5nb9habKM0TEs2n1D5m5//OLT6P9f4CAAAAAA4VEjAwAVtR+yf+eDUDW1XoGIKsZSnIg5+W+oNWi0BBsqVrV5B6B6Q67g8SCxl6iS4xbJTsLDCANAcCVOTPy9S151AHeYisT5mCYNxfR9qdlriNicCAWm2qEA1wnBkG5IYSFtakFxMCkOb//3/////6khcjkSPfavXuRr8u/vVkMYxCxUwUiBHTjTR8UHy4BBYdT0Ji3sAArwKMJknL09S7kDIqhSpuVClykgaIOAcu8yo0CCX1JrFQfQrVCuXITARjq9vn7WPZVjLIaQVZgOBFM739wy1J0lW///ZogZuf//khVC7wWVN//3Ks81jKKOuuaCG/6pUZU71l1vPQ2KRr+nH4ZFC8Jtm3CcyTOnuCT1Oeo5MAAAqIIg46nEjhD6li7Dmn0nzGhU3nscQECRxGkMIwJjBwx0LiUyeRA1v0zHxMpEkAcU0TUKa66hiBUWBZI2P/+7Rk9AZkcVBUY0dOsJPMCp1rCm4QtR9TrL0twjsu6j2sHfixC6N9GWqibhL/aTy3DMERB+Zhmze5P5Bs4xBhs1WkEOFx3NcX6mf//OCwoTFIbEgn////////u5kqhU5rHPT+arr2Sza7WRnnBUYYXYCqh2A1AAAAAAmrRqIRtBAD4hDRNM9ByDpIIuLTHTnBEQDd1ur4m1M565fjFhh0sm4U+r3U0EyFCx54jGv3390DfpisPjeOsbdj/PJsRBzf/5GUpU//+qCWoqrZ7//RcmkkjFOm3R/PM1c1Gny7iROKFsoyTL9NCet5KJg9ZOWjJkRWc2TuotYAAAAAAACqyA6NmDoSlwX3OKweJzLorwdRC8AJg4oEjmoEbRS52QvKCm2jQ4nyj8OCBUEECOMXGLSCAMLjQU4cMLUdt56SKWwsKnnAUan38kyZSIq4aGxnQx8VEhMF2PzTabJKmWBZgd/4j0jAqJlRcX/z///////5U1c155n/3R97GMdpcxKoVLGHGBSrEGbUMAEBIyjj4UFR2j6K0OPCC8kcmMO5BKlK+H1eqGGPL1nngnoahT+zn8jLoTkTiLT2w3YO/X/q7US+axE7f3J/fc0CbkAIfoN1NHxz9TwmFhG39TU/MZpd8vP3idzHluruwdMg/N8Ht1FWywo4aIFy5L5x1GjqrYAAAxIEld13LT+sgEcb+ISZSxJAAlWmWWvVhDhUVpbG5EvCGE4U+0bWtlYhFg5CekPpVMJXW/kHLOgtsU/KWon/+7Rk5oJkJklWeytOsJDrqp1l59JOzR1ZrJzaggowKvWVI6AIja4uxfeKH3anpB2u+8hpm7zNh58jSovAgKnnDY7k7IPiciR3/3///////V8+///X955veqtVgsQwnI0CpkrDKNq1BEAAAAJo4RMcGQwEYQvuXqcABwHmDgKKrnQ4WrCw9RlS+TNyvPNI1V2QCRe980yUu3CWyykeAGGAKXNrv/9udV2UBaV7SZVjWg+S0f/caBbnlq3v/+AUIjxr9CkULA4U7fRFKV1VGZRewl1bK3qf9zUjI01LxrDCPdOG0QBBU9+NizyjcscSS/pVAAAAAAAFB4sPa0o1RZRM0NotGQhV0JHKsL0mQbFlgExMqGA2pWCW9UyDNFUgEWIlSoCCBCpaFeDGIThCgCbhhFszVjZ0hAqkiWw5OBagVBDjk52aZbfuXLhbfOMK9kEKnXEVlejVxgCijNnys55Y//58RzAhEoWt+hv//////PRHIIZQ71/+h753q9Kq+o4eSRhr1HQGJUFQQAABAV7/dU7hRAArItAuxMApuNDgZclDBKVCCbLl+vzWy9fo74OEm5Mh7FwJlqb81cSARCgdS32y97i48ce//hV/rxf+04xo+jset/7ofVLqltwkVlT4QNz+ypMEncV2rRkssupU/d02lTq5AnB0rfuv3s//le47rilAxAANAnJFmcDZ0HXnj1Q2BYUmAmens6DciCS5EbGKJ6M3juXzT1tKe5+nXRvflkD8twbo8ZMKZ0Yk4pr/+7Rk7QBEUkjU40VPIJaL6nxrJ35PgUFj7L1pAfov6/2GHtgZGD0kkqPN58dXkNofj5lqKFrm6rI1DXd0zk65UXASEcRSfz3MPf//////+xKe39G/pTcxKvtrqUEk0bDZz0kCRWr8gABAAABIRiNYsqTBCEgQAhURXJ7cF43Ka7KXIAJA40hUvJ+gYE+kP6XikCho4fIkaHNLeGeaAEyEbdp50sbbkuQYW4FWF8PGfEZm33t0+uUNMpUb/zAeT3CCkfy2jweAaKZr/57yZc16qra7fG/5e3k8zaokeKThsndpPfLGueUDwbr6/f8prVcpiAH0dIAAAAAAHo0UZStqvi7llgp/wMbXWlwqoj6XNEJgO0dtCUQivSziIgo5yy6SFCZaNI9WOEy4sgo4q1p40MLSrCdNJyFmozoBGgI4EAj/mUgRATHo+S/VhuiFL6Aeq2KiGeJNm7Hvx/VwuD8BISHmfM1/VfX///+xyyxhA13/7f/zNnqOqyTDxsPMEpc0Sj3YSR6YICUAMABACj2FTBQaDYKWk+DlM8BO04m8WGZUXdXjSORV0FE7RnYm0ydfrpzgxy6iZnIZTPLqd53qqMFDkNgf+D8ZG5Ycn/8VfLxX/uWHtHR///M/+VSRtNdetHLzZ9OUHzLDRdQivRolB0wDBt1t/JCIeKFiGSvANIU7sKkawzGYl8JKTXvV22FOhUzxwalCqq56oGcW7ikbLgDwsDUpbV+mhwAvGVMBiDKRetEN9KpSjwIZHhto0BT/+7Rk7QBkcUzVay9cwJHr+q1l57YO8TVf7D0Lwdav67WWFtioTXjP9achV8wtVKvdZ/5mv44Woge3////////XKzk/loZuQy+fdqjNmdVMH2CJgsyuLrVIEAAAAAAeDCgvXaUB4WAQqEJRmQyhdMOAA41QkEw0HLJiJkZgoIRN0cMFR+ZnAyOAq+IZFeQ5HFIqVpmMmQQgkwcmMFEmYlMZlrLpA/zAkEg0aFxGrWMNRq132xQY0ZrrAoe3/84+2LQSgTEffeWC8YnCWP5H//9sX/CUHFqNK/+HNtPVNpeTiFX1kB9hMijFFMklCJ83iTX//ioZP6vp53ydgAAAAAQmxYSEqOSN0nSVwdkmJKh4Yg0iXAoQOIV4GsgVgYYOy9Aal4/BnC1gImlvYXapIgYJJGjFW48FFki1Dbksha6kNBKmsOpqqolQDhVpczOG5RJdyh0mYTsigCVNLjDZJLBDgNfpoHrUfPqX/cdEYVAMKf/b//////2Zkmt/7f/6tupo85pUTsKgsOmtxIegSUMDM1pSxMJlgJGL5G1KTEg4NJtlTWX8XgmLCH6I0sIUeh+ncB9b2OEjz/TDIlzjG5VNb31LqB0eLE0G1H//8QxcHQgAkf/yeVqaP/q84VEcgWuD6/n3bgbcCy0tnVtX5NV8/0KDIsOR9PI6Me0nyItEfDwqyZpaGAgIE7AE8k5HmgBNKlPBndJiPbF3Gi4jeykygT6LAWvPMo2gc+rUVIqUrFVNAA8C3kvKY80MfqlYWT/+7Rk9AZlE1BS03lbcJHr6oprB34PGSFZrL0PQdIwK72Hlpj1isuhNh3MVn236lZbdvcjpQ1lcZlHOIB84mZBAR6dBwu5n/7///////2r/r3//pXVHbdChYefzrF1SDASAAAAAAEHBwaLH0yhZMQgVa1Yj1pBoMikp0ooFR5MGJC4GQtcgdYOHVqv+UC5gmDiAdWzzWJLmWtuECkki3qBhaxZ+h3G6CljqlK7//xUgogZMi5oRT/EpU9tNeJL8SUGjT5F6/iMmvu9KLLufqj/uatjaksUkRQgQRzjc6bKF7QaaJBMIWMX4Utf/SAKs0shyI6nhCmNz/MIZM+DQHu+AEgCMmchmfKEpwaeGQOAEEHGps6RBehQJNKwHQoVAHIQGcMn2QJXoYiIQdgMs1Uam0vBTKa0OvuqILOhct0yYKgso6r1RGQKdZiIgTBx7sQyNBP411MS5BSYaEKhLfwHbostWOfJwmGCEKDT/Uff////7f1Y1qX/Vv9kab/0ZNEWPg5vMpKAKAJgDj2aql4uYwjfsPI8w/1/FQMHa5il8qnIotL2SRaLSuSOh9+R/SO3QR+u4LS3TGni8ZGAyIoJA+OMbzxBD6FEr1mt6/ypAK43LT29PnUOR1puZlWb0nlfwkl9VcFV0pdOE10aSF4qUcnUieeBX/7mgwIAAQBAzN2FptDjk23aiKuGspGNYYRNMRbRCN0YEVjjeU4l7lLoefJuDFVzK0u+rmIw5Dzx+ORGKpeCB86EoiHVI1t1TJn/+7Rk8QIkc0dU+09FoJiLelFrKqgOdR9f7Ck3QeSwK72GHtCjKw7c2TW0CpcwbDUgepnXmnhKPjb/p//////9sww84x//++vfmaK+eqicUidz3Px8orUCAAAAABE4igZ4KHBS2YoALANMo8ZVNZh6tzEHDR+ChEiDsUdhazFuyhIFmcbXYoXhKUQYpL7LSCsE7DUaX/+Utmzgpuy7YDvSqDu8oGQDgAwqWFo3lTHLYrMHfR4jw8YG7/5naewlCwmSPbHsdb+gXqBFZkbNxBREfgRuuBVBheKWmEQanMRf+r4BAAAAAA4PAE8aiVM+fvqhON7dpKOBctrCpoSCKgw5wigJI1UDwpvD1cBMeGDVY3JGtljgQeKMcV6hPZTFY2o1VtOFRYtKUwRzaFTyqNxFtKKebV0mt5w3WkcHyERhqD9xIKoPFslxWC88TDpP9af3b/////c1R9dnTmdTW2Wvbeuv5Z2s26d1hK2JlUV+eJCqEEBBIGGFkHIDEAtExK4RhW/Ow6UgtJXLOkyiI21xCps+CHGRUrRlTg0GNB14L+wh6Uzy94QCCBetyChb5k7E0zEgYge6S+JJPi+BICBmbJUrk6YrT7cb/+LIMaQdkzNyXf/9I1989KGTU///6mFYVeuuRagg2qEqnsmIYVMHNzs9s6jxv5mTAAA8KmIrmdDvwyqV0S0zmpA4GlGWwS5U3DDAjfBYwFOmACSQCENQtI9Dk7iXaCcIfJCVghGCxVoyiTRTXGZm/Lsr/eBEJdX/+7Rk9QZkUkdVa0dOsJGMCq1k6egQyRlT7TF2gk+wKn2snbgEN4yFhKKj4up2WWniuQ1FFhGdw/yFqfk9OaI4EwCxCSKCsW/igKiOLxs3//6t////+qSynM9/5jdKerzWPKNNtOVx0wCYvHSzVJRX9IAAAAAAKDgjRFg6ykdEKLpyJ+GZhqCIByYOl0SiC6xhCSgwcDrsIhm7Hknk510NgaHZpopjKIaQbLpxGxu1/wTGId6+L8xj47CJXygbICARhFFLYp5lTy/xwvBVRZJ/ur1NdpQ6ed/3+4sXEiNxZiVTijleqv7huck5XLK/vXZQC6rvS0oAiAAAAABAzLCA4hiA0tAKmz8A91riYiu1AUv3FQyHjFMUNlL2jTsNpiu6zZWdNddoQY3BXH0aAMdiRjnDbTzeK0+m8yh1r6IYZ11lD1UzI7doaolfLqKMEAOBkIgeHbcKDwFAcBhb////////RI91F2p7IVGyMMejXoZVr86gIPUQDMaNOSHDkCUibcGg0ChQawQt6xYK0EIEKEy1CFOVBhGMTgKglV5PZG5eWDuAMSqH+yn+fS4LQfIUAI8TVUOpv++Ngm5ZH2id97XPKg+AqB4pfX/5hUmrv/MD1DYS3ONP/0Fr1z66hxflr7//4p75l8vUHg6xMqJpgUyqchqxIUkuY39v18qsGAAAaaRkAdIXYo3YYecMLPiAchU1dfhdUhSiwUUSFvpQoqmYzGPvugkMqRMWJd0s4kBIWLrjARlekNI54HKIAzz/+7Rk6AZkJUxVa0dOsIjsCt9l5aYQFR1VrT1vQfev6rmnithSCH+FGIQSol6fcrs5ex46bkr5C7JFiLnXalilyPKDusf41/IcCDnL+n//////9stW//////sdWQrJcwdAAAAS9DwuNHYuASLLjzc1ASygBAkQVj4lyLJDYRAhRTJurqxJWMqhDNqLKDOTMxVniQ6TiGKt5QRyHDgCckFjT1GuDdAGxU3Yfod0n/1byPq6kGpyWfVH+YUIla3/lAHB8kkuCf/hi7nS+IKupM//8osXqglLKEYYCI5QIWWG2khw/IBqAmMbE5ECGh2Wc/wg8wCAAAAAOTKBjBd9a70P6Kgn8wNQswCBC26qwAHJL0wDJOHFkqUzGUQeLBtdUzEAoBBLTgasSPWiWmdgSXQqUbgJikOAI+U8jUGgg5WYt6/kQ5YnH0b9hbWm6Kay9fbaRBrzeOH0WJGxpGaVB6tAFAQOhQh/S3+3f////3NHixd//5Dn/zWHaXMMcUIOQPK5HGhSwgEoAYAAArZfToHozgg77otN1OJEz01kHAwGS92kwJC4XTWrV10l5uYeJyiR7My0AYHiYWD6pR+twgSDMina82n5acNiTT+P3Nf6n/ysaNg0c7/UUVU5WioUWRS4O//6bXrveFATD9KRIo/oVVsH190p7ifiLZ/c9CAkgp0Og8VBuFXL8YNK51K9yUf3QRIUbRrLQoJVB27XtM1fl5k0XuTDfaVKZxJn6YjKI8hKxQJBIUqT0OxcdG1FtIn/+7Rk8ABkh0hTM1hDcJLL+p1lZeAPCSFh7CzTwcyvq72GFtFsLjsSmy2+uHIUhQ6KMl2roYSPRv83//////23KuzeT+lNLPtN1KbllUcDGh8QAXEAQAAAACAa/oMBMtAwhiIJCrIPsVLvLIcx6zBbM04Qxs5g9vW53YhLBZAlEQSIIxKN56ynmv4ryLIlVlQV0qeHrLMZx/X/acBCH1uyeJR90IP8PgEI3LE4vQtevOwYIUnX9rIFR959h//vKT00+a5Wcd4v5/0EDzUUoRTIqLiSXqFaDmSUrRkMmItTepyaZo2gAMAAAAABZNpkS5OhKC5Aw5NQcCRGYFk08WSAwMOhxoACvMJMIAUBzVK0bjOdjI4YExIAC0DUYhSutFALCNJx+UD2kvl2J1rolrlzkBq0pdrB8jMok8fcuKv8m/TO+1991xwLIR0qEQIBOGz2ItN1Gw1djW/zf+n////9ccT/Pb+y/9ph7JMXckLKILyCiQ4YAK+E4byig6BhcXHgU6EZAwuEDKPDYjFBscJSADSWhqISCLPU6AqOgiLLmOeRlOjDgwUx6bTtMeAHDF+2Ijw8U7fwcdz05QcE9qc1ikosKbWUTXEsIrYzF5OfjXCQOTUltGr/MWGoPGxAEujP/5UeWpR+uqTJ4Zz8+40e1M7aA5sjjvTcT1CQYn5Ug8VlpY9NRvyge9FU4EQCAAAApreF0oAlI22UEB4ICy2BJczaZrlQYlsps6zwJJ0lNI08pcwRE1mrRJY9LnuG2zP/+7Rk9oYEgkZUa1la8JDLyp9rB25SvRtNDeVtwfUwK/2GHthKHkrjQ8Q6q9LoTD/zMwSWi4y/hg5KCtyJUwVxHGFXW0vzMyYMCWAWZP/7/2/////q6IaVRv/+cpxu33PultD1OMsayHFBs6rdAsAAAABM6jIw1YyZGNhCVcMHocRArnWShmnqtBuyvpyMQVhc451CjkVQUmrt5+qbs4WBZ7qhXSvn/YHzAK+ikc6hTfJkg8DoYCERZ//fu7v/4Fg6NDxRl//9pfPoT2XCw3HFR9szWLCKIpt0qhu70PQaDwfCCfHUIEDcX/8jysn/k3hgAQAAAAALt0cdWdKEkVzJqLvOVguEGAIGSFeSEQqAghWqhGsDIWVxwOAWkX7R9RYfZBOKDKBwKhPIj2gtZIOZI81ev7Xa2IQTc/SgcYUSOQhGHOX5MkgjtyuZErGgL8Ynrjazb9538B4TFAOFFD/+v9qIr////J5iuKGOvov/o3MTvdk/lGgOQXU/oTegUkXSAoShFABJuJIvuEbecdLtFAzzAAtSxDgKiGRNIivggOBlEIDZUV2EQc8dq4IcXCE0tDW7pRiNRBEcLmn1RmJXYtgKCQrgGX///q2c0rn/80iEYEonQEsP//9zIZL5JkjhCjey++s6U9mZXSUMvk8kQtotZjCXcEZLPfEfr7tH3vNARCAAExmKg1AFKllseVFZB8S9pftv50uUoVBacFdEOHWq0JDAFdWCABmmKWEGQuguSWnCDQNRjblyzKR7V5D/+7Rk6gYkGE/Way9FkI1rqr9l5bZQcR1XrL0tgf4wK72HnbhLceqiiQIF21KLuKSA6IlGJvdPslx5BcXG7FEddBcEolFAWiYSG/qW/9W////9srX9//X7X61/uOhhSNlPiSPVaGAUEAAAAA491Kih7OAatOUrRD45JTJphflOQPA1BDjwU7Gw4bIilIeSZGpXTak1bdrFfSivviNvHa9IFiRi3PV43zzcuQY1//xjauv/KTE4oRJ//6M267m2KuUg93/eHg4ch1mFCIIrQhiipA7cx2CgfnMDriPlAMT6flyd+AQAAAACxfXyDgY4w1rZVKb4XGXOjkWoTBIg1RjjbK4grhFCNulEyJpprcXnR3ZFAyuUOrWS94sswl74k194YFcOMu1DaarpJavhD1JP0DqhMiIhcPdGZaBkULLMqskdnD+3D85ipg2UaN/Vv/t////60G566t/+bMm35qFnO9Go48Dtxos8iIg8NnYHgAAUXGNtjRPDA2ZCNNBAb3piElvAW2Zky50eyqUPqp0yqXTc9FigyRCa8UdSEZxtIN8E3guZpjnztfn1Hlgt5mXw6tZ1bL+1ZycIi5I4FQub///7aZdmB7f/UnQJugka///u3bSXrVVSmQnlV+n0clkdYwaIjbMmBavk2KUyCQmDzewp3RhZtG5WAoAKN0ao11k7vqHrrOQkRkAgESES1JheZAhM2cL5GFEhnU9EFECIPIvJqpTIemxAzFJXhiCKJmKRdLRuE0dVVBxJ1nbgtFf/+7Rk7gJj7UdX+w9C8ItsCs1lJ9IRYSNVrOErwlewKjWsFfgRE5kaUz0tAnYHb9mdK47FGIrRfilh2RLpcCTwW/ECxbKeqSjfb2emCKgOBRQp////////1qwwVeqno/t5mRmZFaiNp+8IhYgMA52cxBieAkAAAABELIFjUYQ2AsEAg4a1k/6mVoBy7BcNySJQyWRoDKBapNORlyjSDnQxbirhSIQoTsCYD8VsVgXtPnlmIGAJsaKfwzHKwMsSivFjOpKpv///mDixAje//+kAsFQGM2g////nUf7zXVuevf/1XZvfG1mpMLoEC6SeVFe9sCGH6D9CHi7cMX/Sm4QBIAAAAACBnBNwGJc5gUiSXdsySVLi3pZKUSAv0iqAhyAlGRKiSts/iQM9P1UV1fqLuIEZRpuGMbDac54MHQqsRhSAkiVPQ4dODeaTuAh5L0dDvZMQ3Ua746FZbU2fq2aBETIEADBVN////////0ETP339q6kItiO7spv5pxCIDgYKdyFFZ1wZgAQCWbhXszAFXmrOASxQ95Q6VTEHBlQFQp4sVO3xn65A+aw4GRymucJ0MhCFiEz0kfuonQsITLvf/qOmicelv//KhPi/+AqKCMT5v/91b3GTjVHNXFR8J423YkXYgQRQJZqSxOZksiBAVS6GfWLb4swIwADObxghHctGm/Vg2AxgDXVOFiJQujXaMpsxtqC55+IUrQ4VNvAr5giHNLKH3vgZeDzRhIUw+EJuSuuBwzRHsx08SXZdfP7/+7Rk5wJEXEXVay9LcIbL+t9l5agOQRdj7KUPgdsvrD2GFtHYsao6KB0BgcOlHMm2oEMocnP//Rt/////+gxP5enXsz53fX/uKOPhErEFRXBOAQAAAAxQiEqYoukpEyIMyAUWGgfmk8XkX+REgM6FlhIPJkSLKQUWLmtKjyCy/mG38JfEoeY1D1KYQUhpch+atd/60MPqosnu892/rGzqq/KfLO1B2SSP//9rg1H+7v/yHRIUnXBZ/9yzYrNJMVO01//72Vq8eb1ZXKPK77pVvXl9Y7Y2zlK9O5YKCtKkJkaqyAQAAABliFIiijyekqbK1wLfhiQdMtRmRvFhDw58CizNmbsm+ZNTdU9zOh0CyBqiGjMgQugs2ahi20F1VRMaNzBwuVS1LV0GxplUzjMSLVLkrT8YUElDCWdOKBil22hLqfVW5AmsJG3fZTMu25kzuQ/fuWLgfAEcJCbhZP/60T///+38XGAd/3+0jSxHyvsKD/ysUpWR6kERXF1ggAbLkAOOF/RYeHLmqKWnmPLmDAimKoRCHDBrTAUTdBYkww6fiKEhGtlTtcPumEw4AhAA0BKnMzQrfKuqixATZJGyKSAya/7iwKItCSrX//XsbgQLPv+z5dOAoJZ6nn++LCjUaNUmrJADaEt7z/lU07+Lenvo9UlklQqZlmr7IfERVJZpVBVCAt1p+QmgAQE7ppRKKBcENvJDJpcnfASQKr1lMIJKNASLVjS2gWZfYvyyRPZMZK8SCmiXkVQa3NA1iQX/+7Rk94RkhEZUY0t/IJrL6nxnBYxRqRdTjT0zAhEvqzWGHtEODoVRPOjkMXCoDpDCcxKDJ7rSM7XFQ2DYqLah+6w+XJBdhxT9kx8RlHFm/o3//////3Vh5f0Zkfj+jnX0muXZ2tz2UbBIDtihA8oaL2pYUDIAAAAABRkVuMINUQYwZIANSc49fZ8IOTGL0lggMLAIzbv0jSbjuWAFyo7nm5mJU3xOZTKFdC1kKQGIGuocn4LS6GQTM/letRKdgVJYmWGio///lTkWlqa/+cFueBh+npnT3+nvJ3voJZxA3u+d5zcMofBY/mEiBxIUfb12OkYBo917+bzdfvzmCr3r0/RYwAAAAAAZE0xBGWKLQ8vJYE7GRGIXFHQ25FuTMCS+NJQdLBgQVFDCUrEmAUeoDRqMByasyEIJOTjYoYBxM0kOTKpehYJgEENxmYxWXbDg8aLBxqLvY6LGziSBCwITO2yH6bZWLx+ItRgI6anVKVf7//jwYFOMf+N//////+hau363/vOzdPVmRv3CQ8OF/YwZlCUAAMivUMBXmdDilokgGZmTSPhjaPICEicqwT58WseE/jwocQRxXolK/RoK9sVLIpotGX+N1fM2HAit2eyzd9CUujLtf/+2YxRTd/7w6qSyI0S8UnVv/t/31JtoZV88+y///OS8LxyzMYoiRojduwlTZHcExVB7qkDDqtoDEA/QJEsPdeVvFMh5m3T9RdbGqoz5v2kOK8r+PvCKFvpliTloB2tu8vxASzJZlM7/+7Rk5wRkgU3Vey8z8JArioxl5dJPmR1d7D0rwccvq7WGHtHq9VAkwPrwgK6qR6LY++kdWNCQNRKGDZvyGoNbsSEIlkXsS+pKUMHm////////+jbf/39eZR1d6HN1NYofOyotrpcKQAAAAAy6osBRbFBg2NSDGBHLIZYiBGIAp9FswKDHADcEUVAmWJMuqc2HEKQYZmIAxe1PDjJYTwDIETt8gp/5R/J4pi/mjF/SM1DP2ayEE+VjR//5GCjzP/jSywaMcX9f/3/BgwQQ2PIGnJ17/wpdww4g40RQ5FXCMu6FHVgao8jtMi3ekAJrBqVAgAAAAAhKwQZQTD1UZW8QwAN4iMFjEWJhTIEX2OFo8HGmJDRdMgaPVTCgLkosighmn2wsAUGj05jkJlqPJkLTji6UMJG1l+mAKWsnVuRacKkdKVPJF2uRd5SIJXkPW3gnZS/qYyTMIYly8iXvrlAmD4SBfOv////////yhypXq//wyeyuWZaV8xHZwxWgYIEMYIcBhhKJhgVaBgBaOZ27QOCgEbK0PxgE2FpggBgAa7sMVEmbNOgnJmSARyn5n5pr0LtA0KY4I/9hgbXMuYNHUFQ4I7qjfy9/ZTZ4xmnLkuLDDc8//+iIaIF/QQYKxEiHNFYaP/T//NpUITahDG//C9/rIyEDaYFnBSAx07ZJBDJ8aJ+TsZ+77+n5AohLDpxlPq2rapmUInHKWhk09e46AhS+IgHeMdEcKcLrhgTZ1WsIkylIZeghWsDSUx1kJxj/+7Rk7YZkUkpVa09D4JDsCp1louIRPRlPLSk8QhiwKvWXltgZJ1h45eCyBenY8jLJwhAAGe5WvV3RRNi5JGXgKkvsJUPdlziWcFMxsj3LVr//gQPiQAxcQ////////9RYn//+/V5ZCoZk0RIDAyiCs6DiilVpUEEAEAAAEZnJC0rQaCglWINFQwciafyXqZ7yIKqibmu2hcKmQ2+cZ5ncXZBZn14icD6eu9RXevDb1Qf5VDbVP//6YUiZAhV3x/vUqlb/4PliQ+m4eCcaf/oVP+ja1utzmw/g5F8v+DR6iqzTqKqjddO+i9UMvPv9Stkff0pCgAgAAAAAIB74LWWyyFwm3qGqDqrmUPtpDNBZSreiknmupuaalZjsVViQNQqRxgRiQm9BDw3CTIp+tockdLhWLI3yrJtK5K2HWKnIJ7HeeUQypPHi7iMyxhw8TX/+AINBFMf////////11+n//5q7MJcz0WDUKLe5TiARNSCAAAJwEJU6VBR4HREm6Q5skcZCYigSBjDQUQAUBKwDRSILBnjbFMl0IHEuhdCLdW/ltWZcqsBbtSVhWbdn4AjMNAEYyxEaF5Ybz7+44lq3eiiVqWSv/WCh5O4g3/+rYTD0kOoP//5rp/65J/XzCrH7Hq6rybuclmQ+CIjFZQQYBPW+yXWEjAwT+8tC5fNBmY0QqAAvicQmALNbTSXagWDDLnmlfLmIQRYJIplqTT1K3Jaq3hYVrw0U3FZCYY8OOhhkSa7pwITFqMqjYA5TUFL/+7Rk5YJj7UZW+y9bYHysCt9h4qgSRSdPjeEtwjewKv2Wm6CnlZBhNydQ9AQ9VNLJfMUVuG5e6C5YrFaGckksb8oGQ9A9k81pN7pmq0BgT3///9v///+gePImzWZdr/qdSS9Sv2OU25tb3WdoIAt8NaYhlTcGiAAAACQJYIggyCDjQKEt0JQpTlCDhEFR3LmCyIwgMmBoiMSdgPtqJKwDkVAK4eoTNGIhn5PhLBGjYQlhbnHdGszCdj9A3gMBydnY0v/Y0RaHjnMrwbkiCbT3/+aIALho2Y//G2vY1LeZk/nR/kytR9TFKIaqI6sAmLOL2zFjhF6fp7qBoCiAAAAAypAbbLDNNXy1JIkRxkLVbAgK0cSElnmMjSjF0q1EDGTqGPWxR5W9TFH5pqCcS16nYXCUDLoQSm+tdq1G9r6Os2sNtJZMRFduUy5sFLATMpa/kMsZsOq/yisWgARgoB5w3F5NR1Oae5xowZ///t////9GRD/6Wb+ff/OTfM9HZ/cSFwxgiCAgEi2EYhlBl9l9vklinoB3yYJFpUTOEQ4ZeRY9mefH+j8Ief6uVZXqxxadOYcZMzLUaFk/c/feLDANkceNQXk//CQXLB8R//MhKr//c0Jg4BuHCf/xSuvNdCsFp9P09qWhVp7IuMuj5NGqasmDBiqwgGJjpHLwOoivXcOAkAAALKY2sTKSbPDbcDIASqMhVCSrGXNUULkLiaUXNS7QInUFqKw5RQOBOjhMYpxvpZDR8ljHrJFU9jnJpM//+7Rk5gIkLEXU609D0Ihr6p1rB24PuS1d7L0PQg2wK32XnfgdKF4XAgZ1Ij6boqym2GqISzgkEa/SieiSHWtQtQIlpv/JGpEHRZ///p/////5qDaxhCs9/+jFqW0o6TTH/Zfkyhg2nIAIAAAABCgoALjIPmCEo7FmiECeSIjeuiJLuDBAsRoVIrxjcrcxl2LapOpzMPTWiD0s8cyMp1iyYCAF6FheEXpfafBCNBzA3FLMulq3/bCNP0JLc1a/8exoWFAsL//IcCwiC6m//zUvyVOMKpY476lsfyT1BY1nD6lkw53prnClTAcpFlfw2umYMBIQAAAADxnYcElSNd60oYrCe8Q6kYKAbVNdQZQBDsoY8zWFrMtiCC7lpxmFrd0r0a3chkUCkKGAQGyZxEVijoSZisr05l8XVjVqkjN6MO9SFaXRidSMx7sjURKgRAFGhNBJIN5olFQ0aahn//b/////3Q95h3Mf/aPv1c5919PXM88VgNiCAAACD4qYByNsqJ7LwCMQTHPrhUGPBkcnfegEAGtF4q6p4eh1C2Vt8nSGAHnf66w5ub5Psh1qJmxFjbWGp/hC7fRQGwAtE9l/GV9m5HUwaBB9trT///8IjKKHugcYYLgKhBCT6iaMUseA7sQRunLpX6cYKpF7ULrDLoF3TalKZqhOE/SC4ABpVSwIlsAkqZqRIAKDI4u4QnNkO4ddyIqCyDCG6bKSA6OuRxEvb40fbCwDO0H0V2kJIIslwn6WYsGiwq5kzELCGEn/+7Rk7IJkSEpU609FoIYr6t9h57RReRlTrRU8ghCwKz2XlthjfbVmp+oADWS97RUo8JRMjTgPRKHechsJVWwnbCqFrWMY1/+ocEAABg4cd//v/////7aVm5n+h0aVnLsyLa/02FiekSBmWEBRACAAQAo/2xA6oLAmecnsODISzCyV6EDOZMMmZhEiENwH3VSSb5T8gGSzQ+eMZURXpb0c59VM3hRnUIdhb060KyDLtrgYhvSrcXT7//zIvX/xdOODtg/Nz/+dei6xUxxQaQQZH+91HJFsKCNDE0H4eg0GoHgpkQDQJQjIGDpe4eZrR4pC5nw9E11CZAAAAAwffYvi3Jj0Dq3PCUh11iQeGS8MwgHZSiwRJmABwHFS62DANKXxAAl13cCoFQcGCBDE7URMmJFIJnsu5nth2RmWzhXKhxhrVbCh6Nalaro7fWz48FyzzxK6//kYwsKrf/7U7f////qf//XoQmtiscQLcc+7HK47BFrqQCEQ6AhAAAAAACEyE8xIMGEwaQYIKI0VAJZRUMYBIibchUchowAtqyyIkwKdVNiFB1A/428FimKJFC3FGZa8vMt/TpvA4gY9U+1pKAztbLlVJdKRHdNf/ll47/8XUJBCEzDvT/nrUbXAsjQ5SxX62/rWhQuLjqFzgnBvR6XJuQHkKHawx5lwnwPuFklY+sjMKAqYHU0EOQkADATPVqp/Asgj6n0hLEAIGAUa1ppzA4miYghIhi9JSJBlOmrCxldDWltKbpERZQ8Rh3f/+7Rk6wBkWU/W+y9D4IJMCs1p4qgRmUFV7T0Pgg0wKv2nntBflYLeSlkME+09gtxN8rbNM3qx+3lwXcZGHgnEsdCcWAqeBAqCRMob9XHhoNhkRv//f/////6GI3+Y3Teq72+6fVGa1OgmKsqHQCAAAAAASQtDjIMLLyC4McDlwkizYzGOLxYg6a72KpoKWl6IdrurCKCLoDE56PeMZst3jFCChUGR3En6QRriuwSYMcsT6VlUyTj2yytyRJKQxn//yKh2DYd//yIYdhyJC/v8bKDpQozkRJiZL6M/6/dqiGBTD2cSHa1iidDQBRUQyg+GjnjJN+K/MKWLo0xSAAAAAAAAEDwJAGXEmPDF9H8Z2ys6bmGi4CTSVQQRRrEYcxJAe2vr9LLKST/RYL7FABlIeB3YcXKoMiAoeamK8gCXsVd1IDJt3MonJcuMSirRR1fRcVWyu4MbdqDoaZbLkYHCHBHAuCcFOJxx3yjj0eFjBxvo//9v////5yZtT+7/RyvezazyBqH801kV2a5xAHTUAAAFtPtKIqLyHFQoRkvKeFqQDbM7elPhCxeCSCaMy+kMy+tNtsoVD+rkZ1GJhsLMVexLWv+PUsCOKxhdk1jf+Q1azQfCUGxYC9/xRJN/5AHRdRT9B/4tPyEmJKdJze2y1K8/he2lB9wSTSe0biI0aKGZHdTTEKiX5G/onQJQC6s6rml1I2++jtSEuApav5h5EMZeluJElCZKkFu1bsBPEFhKhhaG8fRh/AOaPVqERYj/+7Rk6gRkfU/Ve09FoJML6p9rCm5PjRdZrJ06Qa4U63WHnpi+oYR5vD/RQ8VBNByu2JGpmIfCbOJhUD+GZLwWBpQkMf7UiYsaVJan///+h3+r2AFgiiorDeFKlARAAAAASCrPQMtFQbmqql1S5Z6XipA5EpYzB0RZQoqBAqI0udJpTWsJSioKBEnEkLEei5EwIEngN6lvH/s3Lh+A3C1DdP1NyLhZ0pUSrFyRxyDg3//zZs//x6BOAUNG+b/uKrZFKPNT5WWGpvJ609+odbKM9cHjxKiR9ZJQcfCBqz1WtKQ+5/razreFARAAAAAAW3xgS15DuNG1oDQhW81sUZDofiQJiJECSzMAfQ7OHFW8darxhSm4KDFtQ4C/qGSHwyALYwGtRiSUNymb92rDNnmgeJJfJ9w3uq8eTuu9QNQay5k85TXIabPdFcG0VgApX55Wg4Lh4JyD3//1/////9TzWz2aqf/duz+K1ceNe9/1rsvc/MEYYsCBCSJxwEEMAUVXo+wBBJ0nkFhBUto8LLwCBLWI/kQ1tncP1FNul0UZ0MM16oomqMU5QkIDpJwqP/hRNqMZhGjsnxeMsvHGp8I5cKPX//Jf//fwKHiCon+P/hl/5GoIVbPffH609cDSwfGEY45BDJuCuOSykHxVvkz4TFHWOWGBBTKyL6k3aEg1hhJpQ0GeL5MkZTRVcFUOeAgTXQXU/ZcZRhibgK9clBtHJMFikNCgi8mUP0rGogzNk8GRWIRJ15VCn4WasBCMsqT/+7Rk8oZkXEdU609cwI8sCr9pRugPxR9X7T0Pghcv6v2VG6CeftLFz3UXtTTbuyJ9qB8h6JYFYKII39HoREQ9FUiZ///v/////p6L//7Je19vYfGiLf3/1H5/Jw+6mQYAAAAAWhKBJKAhcFEqvRIDHQMXPw4FL8KUSAWFQxyGRcEAj0L2QSRRZ3ZpD53a8/WxR3eROlLRujOYeWYxPD/3jVQUKgGpw5MY1+De6+NxtADCpfn//yg6C6/yUxR8BKIERAtN//Qo0eliYqTMa1G/NqNbYZJFipaiBCKY3CE1epav37aUH4qUBWTTQkkAiAAAAAAV3xlAYXhL70z4y0QXigCTqu25xQvyoIgTYKiaIQY/Dj9rHmGzEyECqV7IQAwOAUBIBdk4paRSbrKmVq2WQt6Nkm0iIxFsipjbQl4bykiPpAgwTQ/+tRwAGf//9P/////Yu3sd/s6MJnbRzK0q7nElkK8xuggQPmeIIADr1mQggcDCQamiFgABBJzx0W4ZKYUBu4kMYkDJGl3hLCwjYXVnc9iM8MWEzNV2UsMUVRhMDRgK/WxI/d//96xG1LQyjVVXJOfcu/7cGeJDy7cn/v/2P5OX/z6UoDwHwB0TC0u//zA5+ox5IaXPdTIr44mYavTMdxLTIdpGMBotB7JgrTQtF5x+0oZX+xbm0GLvqVAAHBjVEqUH30ijKlyGjwgcLgwTMOBkxmOhxUYQPGrakYBgjAsMZpYqDZAslSZ8IHeMRkGCKGg3UueSnLTJry7/+7Rk8QZkbUpT42pPIH7sCt9l5aYSqT9PreFtwm2wKbW8tbhKdMWhxBQqlF57kPPWMjrMCoFuKyRuRCMgMVKvxFREBp6QC/GjkojqyscoGoIqOIFvM/6JPQKAK2PFD/Ot60l1tVW///t/9Bndvu/oV1I3rR19XO9NszZumZmr1XeQMAAQAEAJt8dVBS64S6hmlkQMPHSzADL36qDlEKB7EOQxlJzZvf4PoJmM9j2JgkmxiekzR0U8a4efToPJfTRUUOb/8C9AQBSAJrf/JhX/324cBwKiYRzX//YyvdEKobAwq6W+LqUPSkHVjRHAwUD8YD7CdoGDTBwpTGPET9tv/pdoAAAAAAHAiikw5cML8LgKUHl2wVNdixIguQIcg2wWqKHUpcRrKJEoNBVGkaAeJA9FZDgBHhi0o1UEVYdfzKSO0eszn1kOBUuILEls0Z2XMhMVTqx4D2ay5nSfDEwHKrHrCjkt8T//+Vtlh2ikOJP2f/4vW+z7H9bpeGnQxKXQYAAAAAFGYgLBzyuAYcj2AhmTnZoIilUmgxlNMzCYw2Rya7As9y+GlpCQ7OnvisyvpoTjI7x9Ix2cK+qeewfyGUTk2H6preP/v/ichkGTD5+lv/5U+3D4FYVFjM/xIayMthM1GGhpvPdb4x95GfVJXkZQsrOqVliQbhI2pf+X/v/rzpN7TP8jeQWan0dkv1b4lYfDZ6sA5dMJBwucXAAoC0mIJIqHo2yp2n6avRKWoqPM1lHWDB4ZgQkNSKhh9eX/+7Rk4ABkDEfW+y9C8H4lSq1nD0wRCT9XrJU8ghAwKzWXntApK0MMKiWMotwmI4Eqn7R1Kbxl1grB0totDIljmWSgwA4Fp2UT0HxCNB84u7fzf09G////9EQljzf/7H3nNXzdTBos0XFss7G0FJEucoIAAABAWQjRI4jgHAEJgkKMCEMzzRRR8fNYMCCR4aiMKhEObESQGvhuNOqiCl6BsT4vSBm4Kgb51FDFWqCMphyVsef3jfNRQaYmYIDA3/9mWf9JdXtAaj0ZpbXtb/6ik8METXHvnscytzhuccqoj83r5/BM80MGROXOo4eEDrsiYLvMI3QzqFSiS9D/DBAAAACqXeBUSVaRCdAVKcM/gy/F6HVnNiRyhbOQ5BCogGSHXHGHgclbCzFBntAghbAfqRGigBHjHL2hhCUIOpDDYJeS0kRd0DP5T2ZkMoSQ6TWfLtiVR2IcwQ0+h0PM+5vn/AkQPgQVHjW/R/6/////9CL1N/++v4/o2pXWc4rDw05EZBADC8QgAAAABD4Y8QCjwwVJA0EOBwqDFai3XuQsn0Pw5YwRjBZuMqYONN2GMoDaCCbchaLDcFNEYxK4IHgNt3IJgK/78NzC4tnq8Ipj/wVF8P45Q3DEKii36m/1m5iOtSP6ev5iWrn2Rv9dZukOQSH4speLc05yjiAfYoTnv///jJp6Z/bQBEAAuG8+3TR3riwlhhkMjbaB6KqPCQLiERTrwwPA8gCctqcVjhYhSHFOWMgIVQpA/E+Uwyk+j1P/+7Rk6AREX0hUY0dPIIlMCs1l5agQJTdV7TUawgov672XnbjMKSkGGO3KMp2WG4eVd6y4FvUKajG84XhOakQfExkwuKFU7QRHPAJEj//9//////sMkWHm/+Y6oPubO389ZnYdLjRWQWGqx5AymQAAAAAOegGGmIiFLyT7QHFQMbiyWRnyYG7xALC4cvwsRUmcqb+cu3hII6k1KqKGWyuSl6rqAG2aY4ERa7H4XuejYOEpUK6fn/+SyyoggbAmiLCQN/7spN9TwcHg2Ksf/FRbvH/knnQdUvdeme933VyQHmMFxpZwUmodVDpxQSkN9pcG7ExCAAAAAAAAACpgD5lySdRZx7WPtCA6AIEkxxuIYUJQhADMOBTlBQ4vs4yfKp2XpxpdLDMWKD4QCHQ5IJiY8XGQDtOfGITG1J2HAcx52ipvp8p1M3pfgOXvaEJ+ChKBM4HdIlKpUKGL9INFa++VmccPBMech9CvT///////vspf/v2fb9+Rs0rsc4alyCwiE1gQMQAQAo2uaZp4QMIUFYEz2AnrUsOhG/NpaYEDX6jw49YvK2GSfEwcHJbVu9fuK7tIzwe4DZnZh9iVuW24eiw4NGpdEb+9c3hej4F4VwMmfxisafuIMqhwwIeV5xX6FHlSxKe3raq95JYPoG51RDBACcJ5hSzVkpE2SKdbxpAQC3tUAAAN4BoI9Lhw03Vhp226g6EhCcVh0ejCmC1YXCmcByVI5lQ0M+o8YFhVBTfHHp0AsUMi0DRCRJZNGlH/+7Rk6YJkLUhU40pGkI9sCq9phdIQSR9X7Kk6wjuvqjGsifnoaTl7W4gqBWF+0wExAIMp2iGqK/mm24T2ufDCOMGPU96wCu4ddeQR2dhh9XLtS+D85D+v0gVQpTDOlhdB///////7ORJP/+v3+l61ZUVrDE5hktWUBgAAAAAEDkAwHIm1BIVWpPlUh7jYsETmXOmIW9DhjOkjWCRhWR6F68ekMOLzddp9LTKqRaNtaWCMaDjMHr+r/Vkc3AoGFoclAmDROxuB/+o40Le1mE/n//0BWcV/cVD4RAMPhF8vKmyTvd3Uxauzz+OZ5LAFPIl4YgKwYf8uqQ2s//2/EFAAAAAIN5x0KYk9kdpoidvJsMnht83CW+gLYSsaEIgrJaFOxt1mmPptNd9UFX/VKjiiKpVFD5DBAnDWtTOhvakl+joelg6fLRcIpQYSxU150VK3LXxjZ6ecJIAAqUc/TdP//////zIciIzf/1un+v9Y13Z/U4ki5BAkPMCgMWGkKa7BYJOhHgKDK7b9C0EB4WJwuMs3TMa8je9qoqGMAovRzLRpjp6Xkqlws7TNfhfbnNjVxGYtFIU7COoHUxh2kyUz9FrjPbC3jEQ8n7O5///pNkSYoN///EhWWbbW3fD+9vOtWOTn1EMu17fuTqbXdvakeEpIbmUFTDCXlexGUy6cDMN64oHW3sFHidiA8BeQegdR+TmjyRApLBcU0wFEkQIZBo6gYjHFQm5r/glgzTW/BIa7UFELwsUztXiR6f6NsZr/+7Rk5AZkI0XU60VPIHhMCt1hhbYSESFPjb04QiIwKvWWF4CMxlztL7aDTO+yNlThtrGpXEn3b5eMzKW8a/Fo/ZiEMTkCoFHjXObd37ZcwAMJB4Q/rL+nM1f////oQuV9/z30Fj0f6hx/1O7zk7DxUOJ0AsAAAkMAph4BHBIaSlMDDUyzxCJBMXUQQI+mMhrJBgnHohJFHGXItu9By8ChwmYBY6JyXsVJQy4MwopPgp5pVG0B4VySeeYEwwwlkx2RQy2e0+tDj81CgwJ7Iu4dH3//9NKxGB7//0QEYrjqyb+j/Tkoj9OtRhRlqBfI5b1o9OaS/2lowBrNeqERUe+XK0YVUpQLDmYClxNZAAAAAAAe1hGCR74tN2IcZ6QWgwaFQjWRYCIgQsWLNGVEypI5OEsqBoLGCcLjGlvegqqsX0BokuCgid8Xo01KylbrL9fVmjMGDKYPqsJqettwehgEqdBsq7oEiUBU01OymitsYdf6m6HtfW+dHR4bhgm4831dPq3NR/////MaeRVX/8ykoxD/qNzv1MQqqIZo0nqxA7jsgpw1UuqoQ0dTI5Y8xIBBlazc0BIhAmCIp5xJ/VVpZXji4GRAIK8DUuwwsDTt5XWurGpHN2m+3LOxh4VbpE/uE5LKkv7wBEwiHw5/5v4Y4NAiXk1Y7/44WYlXJ527IIPhz058eVkBOFwVwle47vx56V2n+9/5/JU4bFyABANtEQz2uS5T7LDGJinQoI3dFFMhHELzFDaf8qQGsGLs1AP/+7Rk5wZkyUdTW3lLcJJMCp1rB34PuT9XjRTaggSwKvWUl0gXTgIwDMs/EQi5yyYEGLoqnUuUWVnk0RW6+DuzcgW8giZpE3zp+YOQ9JuR8UkQwCgJAWJTrY6B4vh7YSvP/EDiYRDxW+jq///////7T3X/3Z6lP/7ZL9kKZL41o2ppMEAAEAAAkiwfQtgiAgesLSwKeMAI6cTqw+xN3lMUYmcwteblvlNNSZcs8m0YaIg7lkLi8QCj2lgu1kvXHEDJkrXNrof9ARiFJKDf//9v/7T49E81H03d//SsptVaWzL811UuJiDp+779U0pSmsbB18tvWRFROOutz+rj38TV6juLQrAQgAAAAAXD6TpZukbrXaZaM+CqFwVOmsxxkIrheYwR+U0FqQ9DaqEYTpYe2V1QIILlHcFYUhYRUoVdWQhrn7iijSLKZEaFGWSfJRYNJVtSho9ZHCI+CQRBEKHohn4+4rG4rHSP+c7f/////+p5Exatr1fO3V9P7sjmJoXWg47B8J4GAACEL0Ow1I45fUyglLWbGvuypTJp663LSrUsEspzKXTAmVGii+gLTsnKzkMxMmJKTEhKEsKnMlCnDq5FDRPErdJNWMOnP4SCkLG7euX/8hxBvepWKETm6/cdaJuZiC1UZHdBSpPyj0IciHP4wWEQwUQyD0NscPTijqPQ8HxutpkABAzEIVjIMoyp3IrQacmsCaPBadS912DKnjRKXOjq38kdweLAgQ8t+2VS4uU4gN4gaCMIWMsarUT/+7Rk34RkEVBXewxcsoHrSt9h56ZQET9XrLytwe8uK32HlpmGTYutTm+3Ia4v4s8HN2hPIoh72RhgQVYCHAxBZnIW2oi4+os/10P//////9TIq2Rvq1GnSkyHt1eu3IdBE4BxB2qGQGMAEAAADh9IVgUOn+YQBbeA1sjkwZWkqEAlrF8mIbAt59H+h54NcRxQ48F0csNjcGRCBvlsHMzPple4P8rpyGgfydbsQ8WafDooFhgfH//8do/96DSRUwPGMvf1mBd++ZHj7NHzGQTbrcb1fJQoQ3OQU/zJQ0OQBrNPGCJBbfcU47kG7icLdVIgAAAJbCSgC1lcTqyVW476pfIQTL/GbHKBAIMIVxN4JSQOKmUPQErqKA5eoGMAC5YGIwQI2wwaFAjMzFkhoK7D0MAVvDhUJeWC1IqXrFUsRzR8eaJRtYypU45glAJvKaMjsRVzVvdCIrJ0QgGHLkmm/1ZC1AgiFX//9f1F///////RwqGXX7TIcxSTrnX7eToUhwYPRQp7oLAEAACGlMn4XiXKMFu0kusQwowUkChVB2dM1UVHSiVEwczpOed6tpQ4zmrGbTdgQDZFfOeJFUyi1GrESQ5jyY2mV9Nq2FAoCAli8e/5dC/x4IBuTFhAXI/nIjU5xdmHHXRyhp59RoZRShMER4bA8HyJctmECgSAsMNTez9/Hwke8v6XmAIgACwb3pU1XavVBclLGitEVTqSpUVlS+HfQ1hSYBlxIcdOKM/DyLycCiQ8sM5ITsPhlZ3/+7Rk7QBESU/W+y9C8Jdr+nlpIuIQgTtbrLztgdywK/2HlfBCThjLmtRZRlJBgralp3TC2JxdKV5Mu40CAKh8aH1IcaLd0cKDAUUt/0//////+ln9Ktt+Ijtr09/tWykUGWsQIIVEAAAQDlGXbiSbCWoOBqqnHxJmjoNHARiTAjAwMBXBGF/kfpQ8r2zK5CGKljlvlytMRp/G9SoJAwvdKuWzIYHgxu44kqrVbNyhn11pdn6jMVMph66B+f///kmJOrnxEG4TlQgm8pHP/TZv/hkw7b+xGXRz1y+TMd6Kp4ppAlLsNmoJggo7TFdvb6gt+XtKJOSb9Xs4AAAAAAAxwB4RPr4ghuIwBOSHQRJYJJAAQhJGgBK/AyEcCkgdIhB8fEupAtQETMbRR+NPgUdhxr5IUDJS/ehYiXq31F2UI/V8U/V1CxZb8jYY0qUNYrSNUz3KvlzkNigqG4Jf9kqyv5PUMvz/V/woWANHmDqGf///////V0GxJG/0X5FG6/mluq7KMGGDUypUfUVlZcGAhOOlhxxfQICMU4vqnIfUpddYsDo812LF5g52B3yhSM3Ow7wwXmfY+qHGowm2Nyz77bnKRKlhRo8FdKy2e59mtSJxymn//6+uIB5xFHq7fm+dneoodqGU3D65xolCAqjGDop4ugDhMUoHYqxZ5IeK2vyvkF8AAAo0R+0blWvAFCmfHYgs2+l9GVqMVEVasCu2xPoiKkQxxkzNF8jRwkXHqVkJbtUSX61mZqqNYey3rs7/+7Rk7QZkmk/Tu1hbcJQMCoprB34OuSNXrLyvggQwKvWXitiCHtzMQMUA4UlpSuBOh0FfVQj0KQ8mw7YyFSTn2X1geNus3n/3zKQQGai1///////+hXtVfe5Nko/PtzfXQ5Tu4PojAr4CAAAAACRAFEqloYHQsMuKLSJRnpNIcnJXoy8ui1QaHBh1dbntxpQpSDBfCHR5UopAgAmJrCuJYFs6x4n/SCBBcBDULJLAY58RXOSghMc186/+QKVcGJfzN0EA4RA+H+9f/3X6DiTDj5dK4uKqIIng0uBOVAgqg0S/OOIFg7bgqomMaNFH3/QNXdgAAAAAAQHRkwMCQtKoSaJCErecsaKy9hUpBIhyHBgRq848FDYXJKgIUFZYx15CoWposZmRMOKlJVjyoMJQzVw/pb1IEySc6jqbksTBjFyV8rxtHMrWJVM4hJqHmpXT8xlUu35npxnY8w5p//4IQBC2UxpH///////9cpKLvSzSMur7F+3e2RXcljmDCQYgviDBQ0ER0EHF1J3iEYOA2QngBoANNjYs/hcIRj0mUfX+ejndvyn2PBbVNsSAIeDVJ6EmPk8jE3dNa/b06AlCTEJP6Cwv5Fa7aoRKTHXR/7//CESb4GTb/m6wMjISPdPf/37fCv1guye/ds/go81qL/bZfFYFihIsq8aCjwouUD5QTNoB2yPCTRz9LVoIS+jdABA3tnA41pplW3yfcwYYC3NqhMpM+uCBiYxXTYEh3vXs+yu1eiIjvOEDEFoDixr/+7Rk7AZkTUvU609D4o/MCq1l4rYR1UlVrTzTAiQwKzWDj5jpeFjEPyaU3WgRd1oGnpqNKHOY1uvYkcw8Dzv84EeUXhUCwj47NyMSSYEB8XuhhP54llhgKGs+d///////8w4aq81O013w4fPcwVJ/5Db//JAEQAtWJB2Dh1KMAAAAAAQ+3cWIyBDUINgoMv05YNpQoKbxjCxlJihlpKExtndncN076BxdLK8lKpO0uuivHyJEatnhoTfqSCcp/i3OaqkQpqexpHOKqHrPP/4MHk2aWSO/W+KHnVLf/8/P+pH8TXq1jY7viDwmkhyRwOkH8+SadUD+u4iMY4O4c9zzIEIAAAAAGBezkDKhsqgYErS8AjK6yp3XWdJYFXwpcv9pLvRy72zAFLIV3ySL32dQKyhy4S8z0aI4aidNhUwFCYmYZhCOtIXMCBgxaFuaxxR3lL/5YccpVDEf////////qzzVttZ/qpG/v/zO11N3CCR9EAARAKCDGglbyIEX4BQ4hAnuZEwiJmABs1Z+jAMo0BwcMOQ3jlw7MNaLZo5NGWO+9KKpT7TtESSExoM8tt5s5BzSnTL1UBYLPYi4NyKzF785IRAguywDL//1KQG8EIrXp0mFGYDxtBNBH///10CX7r1PtPS+btf34uaykerQTTZjApV5LYjzU5LE8M+JIaha6hB7pddzl60ECBNYLovZHX2qrlMGIWGMQkIVQmMVLXGFMBkjOrCIkUlDH8bxQ9EAeHiShaTbrrCqkTFXKXz/+7Rk4YZkD0vV609EwHKsCw9hIrYS8UNRrWEtyj6wKrWVi4gUUSass+gJvn8ok0VXr4UBld+CZqH3plucAKNEws9OsvkE9KahSeMADgrHQobFuxzKJDB5QNjU2//////////qhkUSjMzhB5h0RnecU77WV//BjIhR0x3UWmkwYxAQAAAuPAROXMYNBx7hmVBh3mFowSiMLcJWcQ3RVDDZzuSio2dReHI8IzTs6TbUMUtSWW8Xo4MKeZsQTFRBNrfcDMUBX///2ilFt/l6s+s2UJ8X7H/v0qgRsu+plEV7SUs+//fQql6VHSFIQJMoxMww6MJWfV/7L8xKMsooSYrBIi0SiDAjAAAAAAwJ37SwRWZpSta8CJZKvpTcSawx3BxToIQKVnKYxO3pDDO4itjjPMRUxCYkpCgEwSwIEkyxYVogpQGg5ul1HWXY+rRQGT6qNDZl49Otv/3Fk+k8haO8p///2otpSoWPLJP/1icHj04OeAYAAAAACE6GQCVl9jGg1Em4pgmwqBQkXPSESlVtGEiDgsactW+Ru3BslhJc5kjSGZtDgIvJuXQGneh6wjUOyyV0E4+8lEAlaLQXHzfSWRTSqOC4oe5PoOMoPAwLC/mRpFISmFjJfmWJ40L6sW2WyccN7X8angSUmgmP1OGnSDFh7pvusnG841ISBppF38i4AAVgeCQEs2bUiw04bBjaG6u26FwASHM04A0whPAg4ABTWCFRCzwpCFzTCIBYzOGGghALwgZdxUQ75ZJgjsr/+7Rk4YBkME5Xew9K0m8FSv9h6XYR5TNTrRzawj6wKeWslfgnmUG8KvE60D0fguGgmajLphvWmwPDr1S+VqYNOelOx4YvFXHmn2TqgWgs39R3+fXsAMGBBQDF3/oK//////+kRKf/ToP7JfR///uQPj9WeHL+CIAAAAKV/tJEpNDGTSAs1KRWq0WIP0/UMqBIyMfj7rIkb0uiWnXa9gCjRjQPiAtlpnoGD6FMcmlPicvPiojycDl/54gUcK//N0SwkuTR/X17H6xfiUOY+Cfp7donq72YThxJruUSPSKYXgCQftwnEmsZtJmGAn978wRAAAAAYOysj8WpGyiAoSDkhAXWdtkTXk5XIKGogNzfpui/I2n1KXVxcjGAUZH6juDuOq0OgmG6U/O0jIOuJWUeH9IcWjS46wZmLeScoDmFRV69ZTB4g5xv9P//////5pKyEfWfU9quRpXb//FBdEUTdEQUlWBBAAABRdh8INhQizJh5EmR/MLWfcaApwNbQbcIlOMgQyeVu0SkEw+C5FrXeamZeUBWvMRY61uNX6F79yp2pTNDIJ4oFgKV0b3Qf8hwLMAoaB4//Dk4covf/M1AcCQLHl/+3y9DP+sU/RnqeCEfnEnbCzU0CCQe4H6aasDPDTWjSK/22oZ3/5RL/rhQAAABiNTBHwSdutbZed8EIAkDp2p9IIBkCQtw5wYEeYQMjKIgEQ2NhuFjAM7cQ4hkGCAAjQNODSBAzEFp60oIUfa0up117rnmkPB4CD0opMX/+7Rk5YRjyE1YawxD0nXL6w1hhbRRWT1V7SDawkQvaj2sHfmmpPIcJHdW0zhcNDBSdEvmnIzcBUr9uxdl2Fvf//mFQqXEg0k/8///////9Zqsn0RNX879v+blS7OUNJlFLnj61IIAAAAEWABIOKI/hdKFyaM7TjgT0aUPi2cqUiGGBQgRESIFDUua9F49HETRY5RdymSAGyhoywBEJYu4Dm5sWU4olcky7HmzsY6HFFM3yq10iUJbjqjf/nFjCY1f/5DewsgteZ//P/L5p+/nGZ++d7acrbkZzvsQdjhQOUqNnxGE032FPjTOoMer0pRAAAAAAAAACr0EQbMERIAYFJRvRSKl7S07ksigIlzTRFWwuSUCFmYWsMYotI1IMYLWqUBxEuRoaCuowwW2hl318owNOS3cqrEjAN8y0Q4yLtUlxWiVm8EPU5yl1XDU7cp1bFL8qXzlAt//xg5wCA5n/7//////+yldKfRT7bUY/vp/5RIznESuUoiIjnaUCBEDAJJ+lIEZNr1eIdVLn/PcGRiODsNozl14HRJdmGYGlzLOwfEoJ//7IWVwuYYQ39FPTdF/26uEbfS3T1Z6l75Exd/tk/fiwYCGBore//Jtj1v8VMf/4aJ+1FbehGEx4uMKcyBDMRiqgPAelsRzJ1lY0u3/FK2V+mZAAAGCEKPBhoGOIHOL1NcOCJEjCO6AiaCoZlphnI+MBSHxJEl9XfVTIWKzk2XdWFWKm8YboDyyACErat5x4w4a6WlLTmqRnLz/+7Rk7gJkV0hU4081oI2sCq9l5cQPWUFf7AUaQi4vqnWsKbmTrXoYoq8KqP1Areuwz2LR5prSJA4l0Q4qDUGReVGZxa/QmOGw6//Kf/////n+rq3S//tRDv6Sb71FchES5Ch7zpTOmIQAAAAAEFbWhpSWhMSLRVWBc49Q8mDz0repPQywQAoRICXPIgD4LNn3xpnSTk33kcIRygb1QG24YMXtPPDT6tQt+XHFAqEEThyhe17o5P6el+naxtyC/v/4QiYXA8GO3InA4NQo8z1KGyRNdcTGCR2/1cr1/n5y31Bvxkuja03uUnRNBG8jAlpse/d15LnGwL/1KsAAAAAAABReNCiwmu6SgbQzoiTlLzzqTLQkojcHGpygU2TGYkQkmS4guV+UOBiMgJh1QAMiIRjZRo0AEr0LnrdZc6/FKW5JMNdC435jF38WIQ2kxEk4l8RiIUrlOy/DyyytSuo2Rg0Zr03OWP/2FRgs7/87f////+pvVE41kJ7zq1s3bpp9EIwKMMOEx46VCMuQIci3Y0RCr+BADdC+ssK51oKtbkt85hHgK6pZFHtcsmjETh76+bohQtJ8CwCZY1Jv5hLMUoIN4NqZruzCLBwAqfQwWLDveJgMFhEIvzKdpUK/GujInV98vyOMHMPVCGFDTxQokAofAMQIrTsxhYZgk//tlGhAESE86aaqkElIy01wgKtSq0zJv2ipop8D0lnMRrvy4bYgwcLZaoe6LroSkiFN2SvwwljUnLgqFhKIwGJS4Rb/+7Rk7IZkmUxU60dPEJELqp1nBX4OnTNf7LyrwcktK72EltFpvXigaFoEo4GjZ0ZMkRkuEjAgOLCgm34m6BhH/6///////Qkh6N+qon//zea0XJE3fuq4hAAAAABE2kAQ0IMs0SklagMMeY8hAEgXFX/SjgRXoyhRKC4lLyu2VwagkHWuk4UigXiMjTTzcKWFDMw1GzxvmA9YgvjmQ+Eul17f/tirN6upf//NkkYMPp3hzpCRieDEP+mc/Sqv/0318rf/vKbkbTuNwjs23ukSjRWkm5NFaB0mWcy0016yJqMbr/Yreu5EofeTrkAIAAAAAMByHo0YcNYeGVtLAgSIXNKgJRVfY4DXMDFQKNGcAhHNVYCgFhrBhSylBDQcMGFMBEUi6gKIouK+RqL8MybdeK/WQ0kFQPgOgaaxeTw06ksUPY+9M9DlZp9Legd5JHMx+Is9i9uVTN/+f/+NUNAqUv5f7dX/////9C89jV/qZ+lv1V1ONfGpquYJTnTy89RaupBLanGQAEVIQsS0xAPGD/dSShljSiT+onBQEajh1KGSPzAtewzhI9pAcJLZSqm0+G2IqReJGmw/8j/9S6VuW6DtTFO7s9/8VA6B4LXO+aQChFUR5vCEBRnL/Z5vu/y7c2N163OX+STgp8ic9nE5hIGMNMDcuDCSYpUFQOF4B4KBqqFe2HudTrkADOpypkZCMYZLKmetwChLF5c4aYqgzMSo9IFdjyzobcaMl0VOi4kBwLxcoJHgx0oZaLTL3TD/+7Rk9IZkplBVa09MwJWr+p1rB34Q6RtZrJzaQfIwK72WHtC8qrA5vBhtChQvKh4FN10aw7VtHSwzeYF7Dg1nkGP+5ciD80SRMepRm89v/////+2aef//7308x5bxvPUBwtGhjGNZVQtVrgIAAAAAJDgXZJiofCghYDVuUpObZlooJQ1N4iWj0XYG9N1SBd6BnnmocSIBbnVb2Bl9EAGDxhKgYEnsmI8fyd/IFRDBgXlQ2HyDt9+H8HRBmH/zcJmBzR//N3sO7/j4mLVbTtVH21138to5WxvtlI/pcS57VYzpwkOP1DprqWL/qQOH9wt9kKgAAAAAAAHi+VGRqBWZPY70FAaU8pknwh64j6jvGSsbjz/1XAnSh6+lfPo0aFIFiBKdbFGCS9WJkwNTAFw5O9MbGqCuKl6DkXVItE+Q1e45JozjtUMxsLIzNIiB/YYmuajHExcsnmv//////0szp//vT+9DTHI81nNNHqD4G1TVnGKQkbSQGCJmMIVNEMMCcNSKHgzFUeDEy0DjCgUVneJjgYACIhZcuRx03Zt10+gSLRX3ptr6ISGrM7lSmqESuZ+M2N//1Ev35jFPH4KjVufLOXjM0H2v/LXTDXu/+TErHUQtOP//NtNGu9qrXMvjb/KbpavV9nTFJAnW4tVunL/A6R0FbVI/56+OJqEJZHoovoBMCzlEW6kygRKllb3BDMNlrWbo8kxKR4VCK5hJcwAQYgoExFrpehSIYGSLFqlBC5gWQEjlghgYODL7F8r/+7Rk6wZkO03VazhZ8ITMCt9hirQRfUFV7WVrwjuuKrWVl4ma8qBcNPCGvQ+j3agGUT7cfjygDQXcctWdzn/i881OEXiWB4XDIrKygsZf8HVrIpx3svn/h/Sr/////7oYqM3/0ylX7kVJrR4khoixSA4VRzaeCgAAAgBtXr6CHUABKOnMTIp6hXRHwuM1lsMsbsQLN2cdejKIHbSbfy47Kd7bXYqmOp6S1ZWvirrcfo//ltDyIR6W3Lkx80RU4BgvGxB/i59C/8cEYBjHkB75RRqRNOeRnnHaT+o1Vt5GmiD0FkdD6NJUC1ZVjLCZRxD3LiFh/TuwAAAAAAQH0O6AZ8GFSOItNBzoDT6iKlUgYakqRFET1fI5wUuZOZaskcFfLuKNQKM6Ok71A9IhJzl/eIN+na3OkrIB1wG+GpDIS7wyCkzLh87VE40AGYedBXvjxIQFlZqf///////7qjt//6JbuYyJdBEf4mHxUjni6RjWAAAAAoxkIUEAkjEP2Ql2i3BnKcMl2R42k6xFowVUC0ZUpYn02zS2UJakQ1/iMTX6j+kHUr+l8J2njGFxWzL9b4KkZ3E5/B4p+Bakv2/M28jK45d7/hyE4Tt4kO//xYHA9oOjV//Q3G1zARmoslVqnzjoGykQg8SNBsoaItLSjRCGBBjAqxpNwZw/iGuFw0CGh8oAIwVhJe+WuLTNLWUHslnAYcjeKBUzTAZyCjQKmw9MJ0gqE/Q9NGXgReQuQNZaGDgMRJZG0QAJ2I7GnGP/+7Rk5YRkA0jWayc2sHwL+t1h5aYSOTVTrWENwjgvanWXltmU+x65UE2CnDNU5dlCoTdH8egxiZos3DdZjZJmyq1ToBeDMc01esT/Nv4WFEi7f+p8robRv///RvsaznT2+ZXn6sX0GmQTYh6EKoiQwHco0azVaEAUAAAAgCrPxEIWan4hJSXITuma1Ixq7eJHd6k7GDIkwLVSrF0ZOKBmAlFE+BUtm6twCOH7lb8igToki9zl89pHVTNdq3pMPs2l3//lL66v//iDk0cl5Q1NtGh/cXTnItlrL8HlTC20ko8fCfZ8/EHw1SOmbTlXM/Hsc6jzwuN7/cAAAAAAExMgjWEhtnEuSFgMmegvYc592qu2DJt8spiMYZm1SWKkeCiWOx5/X4EDy3K5lAmhopvGTD0zof66vuFI6pvTHrJLjWRsN+hrxcfLpNiwZnEpZfNfwnMrVRoJ///4qcFPnThwnfUf7UhAAvNBKgAAAABcvsDheG1RLuAxAqI5AtAw6Bh0mBmfFw1BjDSMiaSEITRa7LUD5WyRAc7DLZRVaKFoBH1nN3C4AbBdeU5M2fry9kZERFFa1jB6bOX2dsmXy1NmUfgOE/vFt1sOtHo//+i5HSoqh///90xabfv3DGYV8ddJ/dLozVwixgzOiSQKxFnJ1hVdsIQc93tadDN+HTgQAHG87JWAgaX7iaezYzEEEBQoQlcXVQMVtMhUWvL5mcc3JshEbNL5ZSi4IgFllwWxmRuaoKRIQOrQlY2CdbeUJwT/+7Rk5QRkCk9X+wxbsHJFWu1hi7QScR9PTeEvglcwKr2Vl4gXeikdVta6409Y5Bbx32UPutZFde9DACmDN36pnHxSCZoZpxG79NxuiofJGoxvqQU0wcf/////9U0WIl//djkV9vdiCwkNOPOwQIJsQpEYaQQElZUgAgAAAAAFnBI005JMNvS6DT4aOiAWuXbLvOeklODpFPkFAE7LUoZ1qUl9ZamPWrYjIjbcnzXMiLOc7//dicvKoJqUQsy+hp6ai5yCGHRK49sP3v/rCQJGF/kKkBi5/6MTMoeduag28Wni9n5hSvvPPFIIgYFj9Vkw2wTEo04Yf/xcj/+7Lguq5cwAwAAAAAECchQ1GVvPlGYCQbZayxhCtK4ZE+iY6KaM6pHjZaXcX0UnylJUSxRsBJyWvj8PNj2zbQpzjs8QoHJZfP56KWZXrtlTzc8N5DGbdIbFt9i9IM31/yuGdD/9f//////1hCP//r5tl/LYrswIMKgheK4mGqQABCCMOH0yS1zUkl2pHPCSAQEgAkDrnGAQkDTBDMiGCSoguko4jDYZ8HORsDGQ8zd+AEooRI3UbYvtbnKDDn0K7n7EM0RliKwuN6wkFSv6zMlhmCu24jrY//9zpYsuir9Jn+JusNf/+t2KfSnLsM5nm/1n8JXLJmIStJomXSslcyiNzH8Dzzo7XRvqH8XI3Q7gBrG8UIERcZQNUIAQ6ZKK60RvC3TC24DKE5wAdG1AKouiNxNR9VnPu9CtzqjDEPNwsJLE4hb/+7Rk5IZkSlFV+0dHEnhriv9h4oxSCR9PjeEtwgeuq32HlqGnK1eQ9Pzq2ibNJvOd45p+aG1L5bDuWFYqqLdHFcRXrftlh1vv/9zh8VFTP/vm//////3uwiRTf/8g53r6OMJQyNEgsWYAWcSWApVkwAAAACXWQq2OCX3a+YEAhme9jByXClzgu4xIKTASyE6QDvy13dSR5FcJ2VOtFKp77ZoAV6W8jMoYLL+4XaCnBsSZLWnmfnT91It8gUByEATydX+VNNk1SId/i+TQuNk6/iueuTSpe+jZebj/3ObGdbEpotPmo7FDYgzokkvRPHPNmtSv/h1V/9NTPTf9G6AAAAAABymQnD51UGg0bbNMCl3Fd5ItBM27gikhAQcAA5PixRebNkn3rbiyx4HWDrqdITEU5YshXDrE+QtxXDvEqfBnm1VamuwKRvgrsnhnTukajSenbEZ3hK2lmruE+9/+FsNdRz9W//N/////oiMR4p73384mcmdX07YziaBNmzngOgjswggAFFuluBAaZWZqAsrMHhYzVDF3W6zjD0GAQRoLSYMhbuvGglDcVDg3ImynagU4aMU3jnYPDt5wAYfU87Blrn/8qeeuCuZf+7iDJEK3x+kh5atT/B/MUUMO8okwkRls1Nfi38i16cogTiNngkOoa6oWIIDA9EJQ9IpPOtXu+XOQfKgo+/JWyACMOcxARpeN52YCOATiYIQdZNH0UqAjBbhsicl7Looji0gC8mK2F4DRE1GM2ifKeKrKK03/+7Rk6IJkc1BU01ha8IXMCs1h5bYQ6UNZrL0NwbOvrDz2FtFhSVLw6iyKKdYot+EuCUriqXqtSJBweQY8y05guaNJ1bk//////+xpKv//6r9/3q+ep1ZpWFiDlf+EAAAAAE1OFizaSBDCagAUMYyKmv2TDK/ea04iCMQNLWZUu1FicwsUCDKc6XU3bp3k50jcSlFdB0mXKsQIcUxNYb2is3+DGgLB/Pl9/PdxcQc7/UOSuaMec+HflR9v7cdaa8IOf3/NLaaLoPUVNOF6B9JIqdZ6TmPJaXHw+jL8O+T+WsgAAAAAAHBsBA5Os57GsLFVyBwoqPR3RGLkjRMsBTZrSayIDZrkhoAgUULlWaX9YIDJFBSaJK8ylOByq1halo8VMRS+Ro+txzeuyvxQ4RyU6j8h+rDKjzQaB2H8XYpoyadUwclwZGxq03aA5uDZZWrblf/4CggFDgohercXt/pT////3W4mlf///I87OcqlPhwxRIWPxIXFwadBgEODAYYYHrBgUSYIZ2LuQYBEOQh1KwhPYOMMpE4mFiLEQwUIc+9pc5flKJ9ZTFLsneNWtsaYpctSFq5P+9NK7q+QDGjgySLQBIIvAd/eWhYgwExrD1+gO5A8qMTyKOj/lB5chljylP2cHWtu/4JKzty69f/UyiXv1Tp59HmuNlUWuk0PZweseyCrrazaZDFEreh9AAALNVUwQZEQc0sl+we87zIy70ABiasZnomUGFwVMx7tcrH0sIdTSL/Dz7OVhnwZ88b/+7Rk8gZkHkdWay9b0JmL6o1rBYxSeTFRreVrwiovqrWXltkCIawgjLxN6sHKG4LAp3SvSYAnRieieXAyB4NbeWIPKoLkwRFMdEisfM8RQqhn24Zrv8TKIjwi1e3Y///////slaoKP/X6/2w4OiAxhI9zCAfDBxxDqID1vQaAAAAABEAjACxdLsIGwGEEVfGOsq1pbhgcHEiazBAYwmIoqztCcpC31gLtNQFnsjhObPWPqcTKl5eKP0EOxHOS5ZPGTMGiSHONybj00dFYOALpjyAwTf3cWeOE1W//9ppLd0TbfPStSi3yv2bzV3/7udS4QQvN1FXNL1ls9yaGqDiYRj+f1s/AROnnSwAEAAAAAAgH6Vqz6xPkSmybDevGomkM5jCyUbIXtJBoAW3Yy+7H37R0Q2dle7av+cidOklZKGFqu0nCoNUlE1TTlN8uBsJzciof7sn4CkWciAgAggJhm31dBZde3p///////7X//prpNyzEMdUex4mDuDzwYCLOCg42INp5iBICBpFPCcPAjmqFks4n8AAZMSGkj9jwFCagDhcvX+oSstkyeTiNZmmsUzQWZIprhlEjkl+O62+gNMLOfd53hsyuESKRRLQSUFdFANlv1mxLlxZ/2/OjaV5OPlv8Uz8Wd/KLFJwtll17//C/fpZ0WkayJ7DbQnUVkqnUpYZY6SneSis7JRdAAqJ5bAaABARGcOkuQo4EdtsFhIGQmKCsyCzZQG0kEoAFADIOk36ASRNKkzQGXip6SrP/+7Rk4gZkaEhVa1ha8nPrev9h5aYR4SlTzTU6QhCwKz2XltgRUpBKpqyZ24VUSjhOk+gTpC1LzPed5U3i22kMkwU6nTAZlMwbaVBGc7scCBr//hgmYFOGS6t2P/f/////onMdvXb8nrXKOpQ16KRjS+FHFBsQEAAAAMAFCCGyI2CBhUDp0g0WWuPpHEQlaRescFlun5NNxsKt7P0BDtKUXVmpeDRHWS6ehtEGpTBoOgXQR/i0ufyHMs71qlIRCx3db6rE4NmcqRoAU+H4nnq//omjWt+rNUiTh7HZWvf/5ikequj5JPEx/yvF7GcSTPhR6583c4oIJrUol6sW1WTf8//JZ/fq1Q/MAAAAAAABcTkBRtBiOA1PEGloIZmoIs0uQW5DEUmVZBASHZs9SBZ2v5SqGlywtMRQdNJgQjBLYiwwJGU1LuwMmBlrLCICVBhngcgYxe0aVjpTH4qiD8zC8B+iiQ1sZ8sKSKgsKCcwRBuY3yZAbmkihQt/HiRnlhsNSY5//////X//nFv/edYzQQAPNZjtkoN7dwMgEAAAAyTcLTkgjAAsQmmKgxkBZKJILNGdGOtsh1YirQxeBqCfwzpoXuzUqPtzGVwDKJaxv8rBjKZ5542NtaBJFMki5/qp/T0ULBcWrPv/7oY080TbrHvEe8JnlV5AnQPD1KHBUcJg9kex/Lksw/4nxi8NfW0kAAkB1lJZLmrYT9MBRsPkjG5XOQKh0JjAVynCAVOmguK+gdhsJeZ0FJtGQqcQtUr/+7Rk5gBkm1BUe1ha8JEsCr9l57QO3TFh7LUWwcGwK72GFtBc7rL5OiWjIA+HVQTLSl+13Yl60pB4uVPnx65SJ3CYFHDCNfupho0Pldv1e3///////////3oCPRjtq0e3W5xZ8QEAAAAASEgwRVaIAiQ6H8kXAUvCqBhtUzKUeC5A4dYuqs9jJdX8WjpILEqtigZ7VnMpfxoreKTaVDst/6ljbcyIY3iXFu+2KVczzEDhOBHBoRmf/bKOS+f93ppibM0n+/DnXLQa9o40u3PLSlv8Vau007tWjLVQTtxy3WjVa2KELarX/SOG8qQeCfGdHmAAAAAABAedcOXkulORAt4DRYBNDGJmhxFtoblTg09CaOiRiROKqZcXMUklUv1boCYqmVXIgKcMiL413naC4liUp3qlFrYrosBAY1Yr9dVK4dhOCXKOpvlYiI66Utozmf8KKxwVvWI04slhcppO31dW//////9qKZJ//8y9fylqsbqFw0aWPFO5cdwAp6nZjQQ3RKlOQLhMMAsXKAtMYv8GA6YKQhkClBcBu+xLLfXybxhOo5QSIhHVwwxcI6CMgOUrBLu/QVXgXMSXNUa4+kGwuNzr36JlYHASAaNf8QqPj2ak5Zp/0T1k8eGKuOtL9XfnTtHCatpsLjrJ9sfzfUpXGY0bS15g5clS9jVilcgyUnj8b1DqfMf/wiAgAN/nrAAEDO8IZt420k70usCWoiKPNosEPCaWMyXMniglSQVC2jUaVvm8SvRpeh9FNg7/+7Rk7gZka0pVa0tOkIsL2r1h57ZSnT9RLeVrwiOvqzWHntkioVsp9pgsfmW1c3MysVrMIMRB1ao3PrF5WFcdhvMDKhLBFZ1K2pFxc3s0sSTP+7DcSxsLy09Df6///////U1yx6t0PdG/Q6ctXqz0qzHmMoQFlHxMNXQfjYUqaFAwAAMAgC670tDA8CAQDjhUP2anwRfKFW3PKcToWEVR+HGoc/AyiUluzO0VMFvVCkjHltdxpvtydnYP4ykbDy+f5t++SaFtrP+vlvc9JA/795CRQVxJDXvMv1JpiU6cGVtzw9/zvPupZG1WV7xfV9ZvKhDFidgpAkQe67X9P2XUFgAAAAEGZsaKDzKaxl46w6xHtVyVaSBERAWQKcwLkIsoT2hKktLefNCNmDgq8TwaiKC+wj7DNZJCnFsiTKGDwSL1mwuJxJjBcrRnyxYNLEMCCIGGgdhpg97yDQ81SP////////UosrOxeqK36N/vuSsVriTEFnKrBg+fwAAAAAUHCUYmkwwEg28TfTuOPTCAUDSshBtSJRqEQstS5oDdGLb5ASJLbJ0QS0HBmLW2WJEIOpNTtM1Xnwa83GflS6saTDLH03lXs757O5HArTnb7/9XwRrIGUNW1W9SwEybn37yWfrIGmppGxxEw3TvXvegU+7nvqmN3Vo1RFlTaWQFCC4E50Hha3JfuvINRowCQAJLOh3SpmmiutTwoFNSHY84qDw0UgAmg3ghOCSI+qtVy/jNG5F7SzKSLJBZ4NSapGn/+7Rk4IAj/UrX+w9K8Hwr6t1hhbRSHR9TTWEtwiSwK3WHqpgOJ2JhErFKWkiw3qE2TCPA737OlFOXxmbmZWrypZTocmC7gpFUVCqqSW+RFR+IgaGsd//t////9eh10IpEdorf9v/lSWREJ0wfi2KghB6LJQroQEBai1AxAAAAgDI/y1RxqDzg2ZiGkFGTBppgcR/WCtNZygwf5OVIp3j/3gEuTrIyzl0nfE4JIcPwoJ/BYW5NCOiEtfz//wIkhyKihV/+xbjFvmvgJBsmB8e3/Ncswu/A2zjmj6ia7Rrr6WVFSxbFc8muyEFlcHRUgfa1DHip7R/vYeRNQAAAAAAgVpAgY2Vfa+m6vuBtQEX+RpeVS5TJKIMI1R5wugt2RBZe2FfDsIJlKRJdxaL8SIvgm4k9lcuWs6oDi2Ngg5hxjqV8JqglosrTgvoa4Pl/DZYLEigCwPEmP8PjQFQrU/r//////+j1Yv////V7KOocVGmkGeXEGkIgAAIvSkeJJeprJgAEMBggWwr2AQwvkBBQMGqSBJqHRoezIvA77vZRlf5QHV49rYGqlxlwNYTJDAztZ4NK53VplkrCxJTVS6n3qGbWu0EV1ASz5u1//1AQeUr7cPiImD/+gvzKezVV7fnt9Tc819uENWtGbQGzaM22iaqHfNNzQYeZ4v//ntgAUm+SiMQV9Kp5xd6wjKcyP9lFcstBo7EHIFAjyzSlljc48qa0u9dDT1eQyOWau1UikKgZU7RA1GrjwRkBWlyQ4aL/+7Rk44RkAUvX+w9DYHwLat1h5aZQ/R9TrRU8QgKwKzWHlth7/LChTyMnKqLscZMJVpPOrW0RnqKfdhbcZ3+oqNFBEBjRv6CvqlP/////T0////5XwsXaESixRBSA+phIdXggEAAAAAABCwlDDPB0EBfvKGUI6mH8SAqUuShwe8tqDGi7K3Gg2ZTj8BJgv1LWiva/qG6iDtrWolSy6ORmc/cPsGeRJpqaun8/Nwpy4o4IB8WisSBn+j/3lDRUXT/mJjD13EjU0ox2tPXvPuXlrdp0u5aZY5y1OthwpEMWnp0v9tqhIIGdW31JCgAAAAAAAKF8NJrIfJcqKodUqR59AEDlEDV2lxVnGS+XYNUJWRGRpSpHEHjH+L9va2pZ8gBCkDJUDmkqVpJtcdSAnshboRmOLrh6kWJG/qP7nKqGvDU+/MDUDhVHvnzBKJBgqqFB1jyWRFx5QaORp9UT7//////qYeYQRDqqZdvn31//+oaTmqreEJMTIZiejX8SWbpUwMBAAApWgRsYLmyzy2gEonCbVYCZBwS47bY7zfhwLImYN1kdvuD7vLCpmfuIexCUxxgUqk0kuyD/h2AoyKAp4wLf3uJ4Tk7ekcboKkttf///q8THgYeM/5UGWWFCRlGFaex8n25R1RQf15MlMUBt6bKqTaCADpngqKm5ynlNmMRn6rUOVSqBCuFSwRibdnPQQo+rQDutbRkcovrDSg4WmVSCoyQKmSXDO+oLxlYJ+CgCSQIXBYeku+8qCBv3TlP/+7Rk7wJkQ0nVeydmoJVsCr9k6egQvS9Z7JU8ghmvqv2GH0gKXa+jXG6tIjSHVQFjccu0zpRuNL/I4H2UxAWEonLFzgXqBGbbalu0zg3Fg+IWT/Kt+pv/////nVOx9mo+if/32RTaXVjTT3POL8wZ1QaAAAAADDjOzsESnRzQlvY/R+1BAC6lmK/KghiAylYRwYyIhLj8a0ppOPs6MibEn60N0H6TbjUhj1uW/qemXLS4X6/zov/DGEruWbL+V5dJIYk/P//9WqYOcd/nWxFEkl44Q6lkHeP2U53PbV/S71rtk4w8mnBZT0DMk8GnjBaN4lpfp9i0IAAAAAAACAsqmLjMJENnUZZEDu1IZLMtwmMpMtUFQhyzINF00/AAwSaWJoQoUEhzf9qyN5tSyhQ1ZCn3AW/EQpFqBN0cVcGi+jHen2VjH47XZ4kFOdDJEiaK0cacYYATjg0J1Wy8iJFG4yH/+v//////7IYpuad+3/b1OKs5MRVIM92FQdKlxY0IB4JhzBEIAAAwBatl2nQitELALKLJUYK9RJUyASYKDKC23Q4vTnfHG6f9sVicenlpiMA22FDx8MOsU1aj9Pl1EeL3LCmvAjZNs8mdYm///Z///A+juLA9kj/4ZB1Cjc8bPci9eT+td+zhvE1Ps9L2IGlv7YdRDSEqTqQeV9s5VSIAGIAAMGclKIZccp4n6oi7C6U6njR2SwlMdRwchc4CcFhRJGZmoWwsA3FeC5Psesxiwrg8IJoOEBwiQYpAnbf/+7Rk6AAkL0hVayJPEI1r6q9h6rRPjSFf7L1tgdcvq/2Hnbg4xXcNxfupEOjMmnjZBfP1JiwKhgpn/iQIwOouM/Mb///////QjRjv///812o+zvOUsSMx8mpdAAAAAAByygIAIfgQABgoAg8oGzmQZKtBHMCEJMwTM8ytXSrY7KXrgvp1FxExm4RFZSv2IFVS+lpMnAKwQNt7tPR/Pv68cvEM0L4U+sgblagZ60xOB7RKiAoEP/8/Ij3///9EwqREauf/1kmlZJq55SafGXut/vs1+dr1IhVMicg9yw6i/bIyVxINutkNs+IDNsUaUAAEAAAAAkZyFJb8vCj286SFYZGxBXBf5Mp5i400rov1HWtrzVudhQeXM5RVYA4DEnESLe5Q8vkim8a33hqLdcBiMthEOs7ootII7qEO9CI9BrUJNKX/ac1uG5KwYEoXhgSWs8/USyZgtcn9DJlb//////3OV1dmX/+uba8v4S2r2DunhYsysB8kNTsUC/QALkwWB1i3JYCMlAwcDvFU+QscAkx0LHQqFZ22eBUenFjfraddYYtS/q8ImjcXweyYHRghFPp8pv9eF+XUgECAUJjT+XXetU0bh14a7NKzucpb3/PWIVjj/li4yNnRvyg0e7zwilJvJVe/7r2f7nskRhdRNbIB56KetpIkAraSKgi498C0fpWBAwAAAFROskIJShLGfCSEUGSHwXcIAHMNIKEhx4HAdCFJEUkfqTOtHNcYcAIwK8a5kGpZUsi21nOfjK//+7Rk8wYkmkhT43hK8I7L6s9g6ehQ8R1RLR08QfOwK7zzm6D0iWVys3QYLLHX0LYVDCfx9IxyUxUGhETFL1O240HXsx/rVKnP//////5xl2f/66Hf/+7rydfPhmnDQJBHmISdFXgwNAEAAAASv9dQaZO4xRCo2FQwA3obMBhtOWVLUZOtd4okSy4fcvRh6cFT2TET4mzovsz5I5vFjI5CJBHQ8iZXNDn2fZ1/jb5/v/8FUiYP7gH7/+kyyeRDOYWXr/5sad7XxAfGk3bDwUjXqB+glAaF9y5HZLdgNhFJvFE2SkKQAAAAAAAFROh4bFx1hkZgclAqmj+z1e8AF7wKAAILeF7yEsbHAlAHSZHRPCu4MIWbX0yodRBK5m5qxOtMwwsWBX5ZxKXXllTKGKlHfuQxTtxia9nfl17TNZLMlGCJQIGwmDfh9QkBWcVf5RN1bX////7/zCMzb3b/mKL/dqKLHtUYvsiCjYgX8YoozCiAgAAAFGQRLgwlGYRAiEkHBoqHdgoAgjThRgLvgKZlgHKHTu6xRrLJ8Fio9O6r95Z6DS3bO4Wj5ArbqToYCaPCJnsYhYXSzNsMRkc7D1LAo1rqAni4+FWXfkCcN1SE1Z/+SliaF9381Bw1zj7mFEVTW0//q0Dv9SlrJG6xBykPFn3ONkIRBAHUTR3o26pWf/7GMi0hRWLP6tAADUqmkMEZmyCXO/oRoSHAIRY5jSsOzEm0XFGkNzGvLYCSSoFSWyXhQGO7DSXKJQlWnLKwYrj/+7Rk7YJj8UpX+wxD0IyLys9gpuhTLUFT7OFrwlOuKnWDm9l/G9aaKkSEeRVSxGFM1nPs/MHSdnq0GtPRPsvf7av1E2bp+w880RXg78Nw1y5OQxRf/8GgPRHGoeQMHvyg5/Wv///rjq8xS6jUxa//vajNZ2v7LNh523GJBsWFCn72vgiAAAAAdVz7jRoCDiKqiVFkGOo4QsyyFlzxtdcFtmKuum3JwtG0Z5O4u3itfq5vPIJhVZexpvmKh45ylT79sap/bxhxoJB7X/Kq5sU3/6hyLAwPn/m8wrFxaKtwVhCeLNf+MyY8c3w9nEFkU4RC57yJ2cOixUogr3rPBrv+6WAAAAAAAAGxtjLc13OsnXLiyLAhoUhaqiAgsSoRxENJSXwepTVuYtCA2gQ21x4QEklGOBRUXstYha58zGLob6UMSGshay4q9bWUS/OZsMZcRVOwohuKxSKJJYQ5LJ43WifEeb/y0YwshDen///pERD/TpMBGI4QedJYOF3yACA6VS4QgLomQGKwCMS5JgISgKGKPDcUmGwg0cPGmcRZ0XMiuDKELS1i4d5tiRmVgcZQ1pwGJPPba2x2Q/dlrXAsIUsVM5zux6j/8iBPhwjlB/f8iD1H42JQxN/wcxUqyP/uzFMXeLQlK7+P6Hv0YXXctWJBocHwx1yU4wPQ7EENBciDjuUFXqMzKQQCCgeaQUSWBHiyhSl0S5SNhQEmEka4yiytQ1VYj7kx0k0vmNM9ZOBRDVWwPRHgcJkKmhedUKD/+7Rk3wZj9EdXaw9D0HxFSs1h5rYRdR1TrTUaQg8wKz2HltiZM96SJCBnu0CXtOo0XrK4zZivkSdEaqmSahcUuJy5M7YxMMqtgPZ2DX/xMBBIqv/l/3/////2scxCv6f9Xf1oZqWyojEF3VRM/caJ1XiGAAAAACguxAKAwoKFQSykOaNYAihYCoUpFKpwQKdJwvEjXOTjDZDp20bQzKKlfDUHo0IiKrO4gAW9YeKM2JuH7TcjKZGqH4s58/l/+LAH4mDIbjSv/NiaeNClI25/Nx6LkoVl/x1b2nVKSszullYqG/VRFPo2nZnkx+KDd5WpT7ci2k10yQTcvyzxH+UrmWABEAAAABKp0oyUSF6xX4BgGVqRa4iGmkwxUyKjcm1SFlDDEkojBqxmXvojE7TsxEKibk6raKBvDCxJI4/gyPThYDQFhOys3ZTvDzGOxvc1Wo2D5aIqkQuOClmVvcUgHisR6GN/dP/////+6XZGf3/6OraJz0toeiKNjnHTR9zXiQK2WXBAAQALFO8RbRCBk5AIAgbiBWKFpOtmiRFHaFUe5xxY8WnlVJyRItd0a1DoYSqUkJUP40rZKsIk9VbvET/5g+Y44V/XGmK1dRocKIiospno2BAw3UdeLB276CiIt2yGDjlEooKwiaVBsGCwZZ/X7/R+wSAAFweIAlo55ZteFygWUIwroW0rciIthCehIWGjjKGDsfqL0n3WJjKbzTIm4qmTiqsoYc3jY4s8jVoegWSTAlIQZ/cIy8jghBr/+7Rk54IkeEdU61ha8IQMCu9hh7QOJRlf7Dyrwfevq7WElxFOahKSgnUF0BCOH4wVhn/7mUeZHcjL9hMRBNv/////+3///6bGOUyHfYOh5BYVEnjSjw9cgkAAAAAgSEgQhDmAOIJ0A4s4lh0GIiClsGVv+o4SigcQDmA6CV+SApBB0GMEghnqBMv1n2/YkkCsRLkkoVhieK9HFquzKXkB1AXYSR2GO/ZEGwP4JcXxf/lZvpDsXn0P1gwOqLnc2/+LQ/5mz8KPc7+Daanh/b3JmtSeYPGtTnJsgUoBMPtb3PX//GatHjHXaaUgwAAAAAAAEiRpYchpQAEqqzx8TEABcTDVOxhhbCUpyzQKkLRHZiwks0xS47piAo1uLrBscTHKDr/Y9F2dr+WCZE5cExhJNwQwsapkydTwojBipUhRNJYyEFYh/wpTpJQcrTHamOI27p8RUJC4sIzKyFrGqqt//////RVDgcFXe1X/9ytk9kRr2ZkShEJxpWxoAAHd5GodCDTMvIFBAMBnjdBApEkiCiyEDCxRAZsKh4WnQqpEX5Y9CnLAC0KWTJ7d5YB3YsX+UikIJDlVGBs6fi3jEGuCISvh/8MGYQJ+caAihAE5HqD6h81JcOQOUwfmzVFAcBAKBupU55oxr6nc3dFX1T7QXnKERQpPW4TgDeS3WlWjQVPFThxDPuo264pgAXxOxUFpLOJgL4VzGGDkR2KMtuPStMMakuVgaKpgxCXN3VmpJaFgQhdDEFsQtK9V7hJbw/H/+7Rk9IZkllBUa01eEJAL6r9h5bZR6R1PjTU6whcvq32GFxGHKcd3l5Tr/TBLEg+Z0mF8aAcDsqCE+pfKw5Eq/tHo0GJ8e43WZvMqUPCwCAJVKG93v7v/////Whiiwpb/+lrfUw5Ogu0xFCJxg1GOHRJdkIAAAAASeu0FRr2RvS+Jo3JO41FFSal7eo2p2A0FDTJGO1lOzyEbF+ZaKjNyySM7TXCFE9JEpmstyvWflMDBD/ExV12qZZ/2vQunJCfLH//OayXz/9POkw5CaDxO2vPLylRO6/76cn3d///5LyxOGZlPZkl7TNOn2mp8IonRPCYu70N/5JJASAAAAAAC5mW0moOhfOXyVhSgjdlIImq7TWedihEcRwSsY0uF4WOpMNBEZQcVeZdiWDrgloYJeiuJhVHKywlGBaOovYpp6mIrqPmdLHEW5DjSRSojFXZCnU8ZCU2u9RNwJ/6fAiKgqAKZkRvjf2T/////6CZDmF3//0tm6FmqyCNSgcMDrJOQTI4cXNAGikvzbYWWi61U1gICH108niQyay+Lzoc21S8fpnK9uwwn4YRE6SdQXIriWVyISJ2MrG51+kQ2hIGQeF2OmL33s05aM7m4//uqr/EiiCBwPoji4gqzBFV0lkFGf9juqqRUZqqYcdxcOzSGHAGkg/+pH/VNIZEQAAPqdbBnul6kk1tUzhFvy1qqkDJ8twa3aU+0KciLHF54qfl8Mu5BrzslX+EFf9pCmlNiOMRfWxRFQ/QAYQq+aWWOCe//+7Rk5oYkKkfVYy9LcIxMCs9h5agOdSFXjLyvgfcwK/2GHtCCRjhAUsQrXhFGBOD4VtPb4ljUgKx4fORP0t//////6HnGnKcj//3Pb00dujux4LRItPvmnjqGQEMAAAAAEq+HCyNFZIgDSvAwMwRIBUBM5QA5yFIER1uIWxTM0GikQ1SRZXW4Z/UYR4xjo6hd/4byyANiyDpPLcpwadByKf/6c3//xYkDTh5Ycvyv+NEIQami5kbHN/KKcHvHN/tCSeNKSuUlRAAKHxwqHwgmLv/Xr5gsPqF9HmugAQAAAACA7FweNt9pmM2i5g8fSuSIAgNymcMgEQwK1T3EJQOFURZVSZLTbglxJmRJypcJxrwC4rAFOzRAkzBJsq1EhReTSeF+T+1SXhFI1UYPpPIBcMzEgy+qBumfF2K20WBG//uOBQ440WKIGr5tv/////+jCYokl9f+dzfLUwx35bkMHUPR1GjwHDXpBACKMgOCHGAs9RlfBA9kRoTZMBkENBAImMIJAuHTHQjemXzzt1nLeNYBschnMmiyp0W5MAh1w4Wy6BuV782o8z1pyoXujcByaAL7+0MiwcGOQn//+BECD9KHAjCgBhJjv9eRljDubV9WkBTQ4lXTIIISyCQCtaToJvx5glaKuEsZ+MPHd/l+kI/K/IAkBV8Qgb5LeY8z2jLD0N0f0IkDShysRiIBUKBEAiB5dAMjMMhf1sQCNJqc3FAp14IxqldZK91h/DJmDmMNHsA8JS5F3YtnMxkDOBD/+7Rk8wZkBlDX+y9CcI2MCr1l5bYRXT1V7Qk8gjMv6rWHlti1yXY3C2qBqGUPkfjc4NhCEntWOFq/FsaBhgqgiouZ6P+3/////+qGOxlVn1/+jbMu4iOO+c51DoMUlERQ6EA5nQAAAAAABDgiABXCRoipCipjgzBvMSErES9Wk3CmLjgYdIhUVE26Y0tnKW+yN6M6iwC01anzVvFAI7IKjf/MyeCZcvmKNfjcQbx/KXLVLBz+TTxRTuE/vkRgLelLEhLEuPsrfMXZqHOOTdHRs9YRYy08uEJTkwYcg6Bd+Mn3ueJwShYnwKYPhPW7tn5UiMAAAAFadxlJFcmkbpqbHNKoy9jwl/C+CKa2muAxESLtNZZAy2W8h7j8NMkbV4UrQvdVR3F5Rt+9zuD509rGKEaYdd8apREsCDSq7TCC2NAQfJQyjz/0zfSedBlGJFNltf/7O3/////+l3RVGW//Ryq7nf6qmiMZOpiqeKAq0QAQZdGXhxssoNaEAY1g+hiws7QPadEjHGir2gigYh+oYW0RF2ixhCTjLNBHq8YZmooLSXwJobzXts7Wm200AzooTVFS5qH7/nZGBVKzUjv/jCxHVr/84ntxIf//0Xy3vQsXK3xL1GotS2VE044NQWcDUoQRALaqExwtVmEGXZF8AVKoStAQAAAAAABRPIehiAqMm/cmH7L+uOJRoE9zAV+RHhTVTeAHqUOGpu4x2BGzIpw+76aQNESBCCojlsVblyNbZO/CvWxxStBrlrpnqfX/+7Rk7gYEVkfU6ydPIH/r+w9hJcYQoR9V7L0Nwi0vqz2EC4lNJ4ZebKGmRQZS03wy6EOZqUBpweC+n8pB5h5h4LhF5Vm+q7r//////qzUVv/5GV+8zzugqjl3daBwJ2IJA4aIIiIAEAAAEr/RjN7JUDgwIPDayMag0DGc1Q1uTjLIGsoWNPwGG22xClU1NLp4wSsTOfrXP4vlhQT/IEdjB3K+P/MCphLIWov/3sbH/5YQAIZfuPf/588bpuP8rUaKxfDZ/YjLLipPJtemxZYUC9IwUuHrHy3RNar/4a3+KPM1T/btyIgQAAAAAbFexQ4TQ6tPmoLlKNzD1TootouV3U9kHU5c2WvWrc/TZ55aa/oW4qhtl5YAYKiY1BqFVYmcptztWfEAmiegzp4VUqJoFCVzB0zhrA1AV4Fq6bL/mekyKRTiX7vz+zOSuZOjf/////0RUPMjf/mOmvZp/dG5GIrBFUMKYg9qAIAABDyJJzisBFmS4ahqPBBagoVhLWDgQ/BrOSKTiR1YAkLBaeckgRhpmBOv23zXpuBWgMIEFyJEswZxz5lib1q3q7VrTyg+Haf+/wKJCnXD8Hivk+hnDFFRb/gpNzcey5X//2Pk7x+XN6/n5h1vh6/xoLUrmS5IUbELNdT+U06n5M8wy4j2WXMAAAAkvKoFCUC2Lw2y9tkkUQAxaAdI5XyIkMDRVSBli7zEhajAV8PqtZuL3MwRkyDtIRgphaYWaylgSELhP/H3cjLUIhQSKVRPLCCZDSz/+7Rk7oJEDU/X+w9bYoNMCv9hgsYRIR9TrOFrwi4wKvWCo9iqHmmyGiir5vFLcYtOMzbNDEV5ya///QFSwfYW/mZEdP/////90v2//q21SU2y0jRasx6gqnLODylSyy01sABAAAAGWYYprjNRMIMZBABQAFAuiRwYqRAEohkDgUwRoMtVUh2FqJuhnTPonPJHlo5a2Iuc0FeIKQaA1aYbrj/zMQV6X1VwxCggqP2OfOEAJAtBAB1y3FgR4ThaVG8jkYhiqqW/ozD8A2JFJ1uf/73uH7NWdkhXfuQEAxAmebteEA+f193692BQAAAACi6wIAjY2zSNtsnCPSTmDlO4IHh5lhUJJbRWuXFkFDlotYTpdxDVFRfLZ0nW7qUJRF3lQpbMSMoD2OBFqE6TEyDBJKN1DFwxXQ8lL5kPRZfOoRBUMZElVPns1t1IEseb/4dAcAjF//X//////dXIIopdv/o1E7erLYjtDxhZBMVHTmILkT+CkLRg1L1oyTJaFbTWjUzARbwNxS2AtIOyBBRdASPX4m666LMciUvVicJtf6+C6HXU8RDpIPlQRq///DseZuoK49R+ZK7/f/bIBUZJg1n9Llvmf//9zKMeKn7jX/rYzNqSnmniyhJOf/vd+bWXv95KlXbDsG0iydPKIwWB6cxbqv///I2D8XX3o9oDVG4oYIs3N9FDkuJkSQo7DIOhHQrAUCtNchgSrUKGZYkVSCQ406Khz3sCRwYKwNYxc9RaneZQJRmOpirNwmEMnnT/+7Rk74ZkOkdU4yo2oIssCr1h5bYRLUNVTKUbAgswK3WGFtiZQ0TFxHcjEosqtdLoiGBbWjweNoXdlenpkWGBA5///7/////9XILqhG//w6LI9hcqq8liqR2YRMyCIgUg5LjlSgAAAAAAAAyXEXVoDwAAKbEFzlIm3MgBbA0x3h0dkIOODCGCv+pRGmn+hmmIdjOrMsR2HSUwGgKW0Yff3jz4BcG+fh7ps71Jv/M055pCeLr/Hr/e+//8TQjeFMGBakBV//GG6I9YLb9nPbNX/tfOptdWX/mSm0FJt9snGYRcoUSmgScG3fs+SfWATAAAAABeZ2vBEYMZPJlp4KDkwkelU4CCkWRAcIYRXmmFBKmaGEXZK/kLSqWi90taUpgrhY7LlhU5sYmzRpcZgeerZCWAlfI4yNoh1d7A0ZQA4PEhqiUTrut3/r/mIcodwL5TT//69/////9tJqf//Wy+vqqTWp0tdl0jc0KCSRfo32GwRIvkaZLxmCWnCUEJ0nQnDA6UrFUcQI0VtDiS6jsyduzjbkicqnD7P26dtsKesBMYMkGtS7ifyp98+QY3DcfKxDZpv+TBVkzU03/8CL0HQKDHrrissWBh2k7/qMfMDfujTJb+PyuaR1bGiaHIosVFzpHPqMw/WB4xmLcKsJM/pazAAOBsOnsBiSFztlGRqWnRwQQGnaqqEGFEvBeoFqErBhEoSEJgGwJAC5yNyk16LCA4Re8eEGJBRTa4mg3qgC/JgM40itL6rS2KG5pqlJP/+7Rk7gZkPkdVey9McIOL6u9lLcRQMR9VrL0WgiywKr2Hntg6FiOOS7HoaTfwXssR1kjci7rotpMkXPX/4t9RqUCYg/+37b/////7ohl3///7fZkz/EBhdTBuRU8lMF68gIAAAAR4oCFCJhQSXNgxAVK466RWMDBUkFjpjmABip8iOCw2Glouu9mnQZOqpF1CmFaWQmHRxNWoeIzmG8LG4XDi7xUugo1jCHqFc/deR+vjuTFZNfthLyaA9Z+d/q+IGkLmG1f//0vXL7CJMtFt3/n/aXzVOnvUhKCJmCSBCiSZqS5UEUBMs6+J+Zm3bvUsAAAAAAAAAcBNHMAIHVo9ylsygRt5pkA4hEcvmDBUQjcTPNlX5IWv4rcPuAuOPfuuCh46zouojSM0mlIGW94aUsfEBpwXE8ypkJ7uqpxlG9BaLuPR+mM7bmslYS1dsKuLTvs/Svg+GgOgQIFADoLr+pGWisIw0GSUb5f/1T////6Hu5pv2//ZtNW/9c15hVaoXRQ6gYgAgChuHVAuAIAGuIrobOEHmpplYbS2FtfMAQZHGmX1hPBRFzisTi9RcihiIomXlK0TPf2u99tWuClP1yYMPz+/4dAha5/IE3ja2+PvDs9m8j/97pR9QcZpAvY7T+v+K+cRDKgo0WkvmRcYLh4DgsIJ6PwZ0e+zZoFMAAzm8gyA0rPe1yV+SsUELlIgsFVSdhEddjTl2JKBzHyrEPXCfJ6NsvJkqkYAgEx+LsxnjLEeLDhEcII2XzBA/Zb/+7Rk8AJEgUfUY09OgJKL6n9nCqZPJR9b7L0Ngdyv7D2HnfAU867q8e4ruRzjCsJxKHx8k/RcoEJNTS1G9G/+v////6NLGnE///P/dN/Tj9JqnHLIEClIICAAAAAABIVc4yosyBBhyuS8yryNcycBBn8Wm1Vb5AXWOlcoMrYyZ3oesAIC3Ism8Msm1b2MzskRrSua5L7vKP6F/ogWBC0Gyw3ROlDPNcm6bKLvI3CB6P/G4toIowQ5R+GYszyvsOIa585XJlWOZ3ReW/pZ+88GDlM5Rw86zbPdGgcgPAn/37t6KiJyQAAAAAAADQs6CFgCPDlX0acwUcpZrOkgCcybxa0VQNUoxxzDFCqYADTAEQCDL1PC3IgBEiTJRV0n0yEUDAzaMrSXbShV66s8m+lxGISqFie7z6Q0s2GZ2MzUKmnRbupY/LQ3PLjUBsUBgUXZ/ia3lBegatvr/hjP9f////9LMCUcK//+qN8/OIUgy1Q4shSAQ+cQBEBo8gYkl1rJrhEQBkRGdkPqKZBNhAIW7jTpMVMkEEFkRwiNldO0ydpYKuqKl3l1Sp+nkgfO+CQiQKEOUpzb3kXc/iyJkZyw3n6eG/pfRrMThBJtdT/xfiNAm/j+BcOWNyG/moFx5jJKvUq8XHftfFDdezIE4eihEAWLYfRBi4cmjBIERPXrYPqrMwAbE3GMuQKBiAWGBgS8LhwEkcxQvUHFDCwgCGMs+CEw8UDibul0w5Mtd7hakxtS0xRYCJzQRLFJU+EMAkL/+7Rk9IZkZ0dU+0c3IJaMCq9lYuIQ9R1V7L0WghwXqdGsGqBT4BhhJrXHifUtshoDROWwxwbDlNeL+W57ESC4bir3sMqZ4+l1l7ryuJJhzm9Op+X8+D1DemuVf/9G///s4JmBj/3bn/og1h0W7ggAAAAAKDkWBhbB1jgJMHLFuT5FDi8mFMCgBmY86GbNCdSwryW+9DPWCoOhEDB4cWGTFlD+FlXcUYi1Z7eYVHRdBbZfBLegc7UV/4xFgTgTCUMwtF/xqUY/RuArg3J3/5KYbPAubkRJAs45ZvlPmbhv6otyywyJs2yZnUToNBuh2U1gIUV/oiHAAAAAAAAQly3QJEDgiYUmBoi4SpVTFJpJtcxePph8xRNwDCTRSya7YDqwczICActq45lTcxhTVZkyZYBiZYR3PTUOVrbU4SMuIWTT0SX5uMCBHI4t6CWz+Im1Usr3JMMKHR3kCL8f4QODwUjrf8n/////3/buhf/+v5ncrL0QhxATBmYR0ExoiNuIQCCoqyIlguiBhk2kJSqR7HEQ4EDVtiCb6uEUBapYqI7Zore3ElXUiCAOIToXMDRlgHuTTdSAkrIVKmX5PRIZTMuE9Shj502d/PPFIgHQIBgLfVzgfiovoTzz3EZP9zXep1CrDhRzCalf2m42lvMIRsCOPlHbY1bGBkH0K//pp1AjXM6mh+vxAt9G1N2thchdSGiCipJRFhQQvShwSRTPaE6brDQ9d6EpGJp9o4padZEkMr182ptBcFvpNKnzry3/+7Rk6YZkPkhU6ypGkIrL+r9h5bYP8SFTrJzawfqwK32WHxBkuAd/E4dLhTEVbpI+VC8ZwG5ibGA+HmR06cinBOVHQ8n/7//t////9lZrGr/b9P/fqxyK5QuhxFSbmNHhWlWEAAAAACgo4hQ4gFEQi9woaj4bsrSzFJEgqMvsITBEkhcgkRLjcah+o7kcaIkoxMkBeZIxB2hIQ2Ujx9t+trW96qf2qp0K/RUZZudee7Rx8NhwBajUVBgX5wwTKYnhcP82ysoE83b/RZ1QhcyD/eDU3wr//99aWhIgElNZE40gTOaTTKkUNRf2/Z/VWQAAAAAAIB1Vw6J74PlrKYEOAdIwEBBxa6A4EcNZkJajxRnCAAdTYdDLboCG8FQRE0o6p07QQINTpOofFsRUhSyDmdl7ZLSNSfWIzbRErJzkG3n2i9uusZ0GlR1I9rjcYZfK/AT8JqV6Psm/+3+4BwIowjP+if+v////+XR////769pstamo6doWCeUYtWWxQehNwWmIixAKmjSIKBNFMLJLXNDRz1blcvSQAuuAGCoUFA05lZVrNS0wZhWRfAMzQSRZi0PYooMAL9jwsupat7LKngMvIaZqBFZthqDUrsY3nKXvk1RD+IZ9/h4RKog2Y3///ERQCpQhC9/9EhGUEaLpvAVBC2P+1PPn/uc5QbSmgtO4tCgha81Ukd6KATB134EMJ+t6AIACIFjxKG6V6x0EyHc4yiwajk3doSJwsCssDMnU0LVjvi7IWUlwBkyEAXH/+7Rk7wZkX0fU6y02oJJMCp1kSfYSXR1RrKWcwj6wKjWcFfhAmkYtAgII+AICAoQ1FbxAKBbdxEO8bcJb7/S8uYHChpy84DbhWhFZmS8+uQ18UEuemik5bXm+6iqMUpfWi/db88DB8LGFWnxUQL//////9yvnN//6f3ffdD7IJC6nMkqnFzVoUFMAAAAACo+GXF/C4IU2ZCoc3IIdmcSVDB4TFC76RzGGVO7LYzJ/bi5ENxNa0y7LwsDoE/kxobp+YHitUqLR8DZfULoO5ieBELrHknofRzWVv6DU8Ji56H25xJy4oHdFKEhw3Ruf19ruxVjo4ddDjR4qBQRgdiTb/0U8fHTBv/dMuBqAAAAABgbji1QKCl72HJEwAiQovfWoifMI+MLWqtRFB/lFmm11ArbgqNrcQOL/rla9CIw2yx4sxPVytrz5hhHoI7O3esWdxcD1ZXjng2EjGZ6zxY6+5Ob//6zvkFAiLiqIU/qR///////7DFVhX//OlCW/vrpnMMOCURgpRSfGUAgSrhTorDZWaBqKwViTrEbiVxEYrFADM0KlgplcS87DqbPRWuSdYmpcQH1j1COPo1/Af6zDZh6x3GMyw70xH6TxjCSMlf/+o6c9///SbHnOmlZV39qbblkX6jK55SWb4/3s5+5Ke9juynjKbNSt6y6EyYIAZk2fBDmwuv2gpALv4Eks1YA8BAM6Ikk5KHZgjDZI6hfdPVHsOIGCPkusUK1sTKvGooA+QBeISwCBEBLfVoc1IhX/+7Rk3IJkCVBW+ws9oIAsCv9h5bYPwR9drL0tgfGvq3WXnfEtZFYXpDjSf+En2ePpIqc5Gp0fy2gNroeciJQMNPf0Rx4iNxMOTWf///////93TX///5rT95yDqmHkgXUPIseVMKhqhxBBEAAAAAmbgaIB/i/xCVmNBUgwyTAprJ5PEZ4aZJgfJyHIcCji6kJ+XBD2U7VcGwZbeQIL8SzVP3ONnTK0hGUqbCoa6VxbqTA9AIYrf+Eym2Kf/wGBcwODhjXX8UtO9Yx7LFhzx/6VtRJtbSkougBRGVLumH0omD4IyhdFZQxKv8WhkABAAAAAAYCy0QLqnOnm6wOPNBpXeRgXS2hcxOAKveUXUAXExzwY3Cd0iexAaMX6R2ZwXIL7jenhXSLeX06cReRbS3piLNbjBAV/1IKf7MvdPs4ZXbeK4dJ4k/LwNdhV6qLYiS7hWsTNv//4HgiB4Jw8dNNZ//zf/////slKN//6/397tmGEFPE417HlyCgAAAAU9P9Ae/BMKgyhquYQ7LFXM+j/OsiWlKNOvEpFORxvwcNni53qIhFFqqRUy/SSRiHF5Ly3KrPz4QsuhChLikqNHQWt3/iEqTtCmPD//ZbiFHw5Ff/IpCOCSy4N/65raYp3w+WpH2rf+2Hbe6ijlUVLLLhtZquan0zFBBpYmTE6aJ0okkpxeHMAEcOmKAKAw9ostaRFxMSXK73SSGLsP6X3N4lZVQEK0gEuZtIh1izIOygHTwY2MmRQGirYL4pWr2c6XJ//+7Rk7IJkGkdWey9C8I7sCp9h59IRLSFRjL12giUwKr2Gm6Cu08jG2nODI1Un/oPq08fVq3Qw3ZqMtjsMJxNNpjURQsgio+p/1MtAZDIf/f/q////+9FKtRib/+vn1V7bdXjPdx/9hGThR5zOKMhOeCA0AAAAAAWKxA6ZZxfQGMqAozTIMvCAlBWTvASBLxEbJehfTcWVNm/TIZ1Am0oiJlWTBFBYuwQSDBgkM2pjn/fa8xVQJSyGZd+n0tftH67ANBzH+YH5KT9f/5ucD6O4dzIq+Vv9Mmn19JpqYosKlv/cYf/UVdsNCStJQf2zKhqTgTAaHiOoqf7e0naRRTswYAAAAAGJS7wO2/6rXgeaBQ1rNy+qdQ8cLDacHEGzF5TgAETSugphil7AmrIxN+PZDtpvkwx4DYxHAGAfErEKIU8Pou5dk2ZSUPNATYM0oz/S8UyWBYjKYti6UCvZl85IRit+///8DocBBpf/Z//////+wmQPCYxBAn/6CRX2dZxqvIjCSomw4JjCFig0Rme2ABAgAAAC670CI/AHAgMIs8LRxoQnM0zeSYgFXqD9OpWkVAMVt00ORWNM8gXKtPQHPMqVVQdddp7+TY4QYZFK8Fh6vYO0ezQnk5/+osXprTz/5MosbI4OW/t3rJ0uqHs1yiyDUee9/uUKzr7SNNpMR3F4rcoYa3EUzCyNCyG9ZOt0peHW1gIRAABhTshErGURE13kEMrBU0jGEUihjIC5zKFYgUBJiupuuCH2XQQzbav/+7Rk6AAkc0/U+ys+wJAr6q1h5bZQoR9b7K02whYwK32GKwgb/Q8XKUrl0wmMnPAz+4tyaBLbL1QpkTBKRRXrpCMyQGJdIr5gcmyV8iKiCA4JqHUtyUjKnigv/VzDv//////zGNdf//VNTrfdD3PJlQqgsiYXFtTnHpUTjphAQQAAAEAOP5BQbJU4FGkyUTqQwA0TVoSOJy6DiEFryi0xhLcwv3Wih+lh9SH60BwIAyh6m3OyW+PAHyS6C0p/UJJW1hsv/6667puP/4IRpc87P/zKDD3SCdvW+Pj+a3vRY7PFi6NapidWziFm+VjYTB3FiC9loZETjFomBDXpiEAAAAAAAAQHxGNVdrBf55GVRkOotyGmrLDRKaICBzzGVaIdJgErU4SiZWF/F8HkFIhIRktp2hmBUmsqlCeinP1Qnml4CCrNM36wh5bEOXKEuLS7JCo27MZ0qTgm3jcPX/5AY4Iz/1d///////9lq///9Nb7tuFZ5xwQEcMcGVIkiVBRABAAACmryB0P3AMODEQ0HQwgcyJBEZm0MLCLziST4AvXy8oo7S3vWNiRR7n+sWJwjFBABihmJvre+9WxPGsbyHw3lHUkf6kdxGJTBv/+0KJG0qQGPtbOa5kMMp4x6/9xnnvHoGIYllf1mXfvqs7dkJxeIeVlWpKvVqnI4IzaQnf//5agvP/4vUR7EsgADQ6VQ0vg3w9m68uekySU+GHwKI1TDArEDgcAAVXbaGWqUOnxIdg65BZQtCQCLsTXIUz/+7Rk4YBkAEjXeyxbwIELyt9h4n5RqUFZ7T0tgjewKr2XlqCByAZweLYhrSEeS5RsoCqawpxxtiliq2FkvOW4Nse5CoaFHBCbIdkWQY/EdTLkzRN/4GgO4UBBp3r1tUTlI3/////srldFf+lz6VJ3d53ju4m2oW9zsZzTCdWJgYQQEAAAM12FUAaY6pOstigAtA4pZYt426m7vjwJwPhJhL5ydScqBGQ33YSsRDtcNRjkt7OJRFLBdT0xF/DniPdnf/5LrH+02Klh4e8/H+0IKKxA84WU3nnuu+GS06Dko8qhaDhojho8VMWDoUXUK6ItslkrDgJgAAAAAdU7sjxW2X6vBDSiLON6sMnuyqQpxkomwCozDmUCbT5hHWP96XE9RbhFAlZCmxODzth0jVZHXi3TpJcOVPCe0RUd+n2eFNCrAvKpxJgkG5h7HeSIEiwSuetf3Uyd/////++yueb/3/61fSXV55Weczu6nKrxqHPEAAAAABHa2HIhCAMYOAoABEmCnXZFY+A1uBwwlNiAUHCAFCBACuh8xIvi9ssMcDGghbBOp+V4yuBmZqVCEuuuFQW7s+zeZcF2GLihNv1IXpFCICwo6fjrrkX6iStaQ//8wKgVQXBXJ1ag2Q0qAPFtn/zSJCSG8IT7xOe/8v/87+lcI0qs2hLo8LjyAqs2QraztKA0J3dzHL06YAAOQgIJYZEQSsAVDFADfZMIEt6q4qZmIMAURyQ2kQCIh8CYl0TTBhAUS/T9FvDAsxxBRAX/+7Rk4QBjq0dY+wxDQH1L6u9h525TOR1NjSk8QluuqfGcHfmw4hGTiCJXsEhEh6j0jW468MsFW0sCvZkjHuSl6n9pXD9p8ofzKAWnsgcSIPc3ysims7O33tnOf/zY7JAgD8kh3+pv//////ZHRSo5/+rrTn1ak8xTiBhhw8yGMOKTxI0ulegAABILzKm7hrGuF94geAsrUPZSIwH1MQUwEh4eGJ1ncAJVu/A7KlnpdSf+qOv8wZczFho5k/LEzKuW4Z6QBkQsz8MwNGWcalVmeYRK5c4eNv/6C8SRIL8x6h4E4KIbE48X9CAmMhJ54RqX9//+uv+t/OJF6jVSqwlnKmOEUeYMd3YDVv+TuIJAAAAAIb6jy5FeQ1LIzDYWI9TLY+pFy4GYEHRC6XvUMTDaY5KopcwG+26di7mpI4xN9HRQod6li6QT9yq8LyqgvTKGH+iQdk4JiMajwYBjklQDUPGsfGG8xEE4OkZn/o3//////7m3Zf/mX/+h62RZRjqHCWQFTqkpK7wVAEAIAOvYZGMeSdBvGfJ/SsmsiOxGUvHxZKOy92G9fmdh+eiPcaTX/Mw5l70rllz3tOlA4YXAUHQyyt6CcE2noG4f03r//qRN//dmxPMTxmnX/82vb7ONqaEpV23tJBT/t2MKTinLwQYi0t0nAcBA8Utr050K/9EmBRF3gxHOdXNAJMSDQS1oT3MMS+XmlMw8IqnMzIaHIlqspRwmajqKmZWoE0NOVyoHZeiC5l+gYHHq8/N0OhT/+7Rk3QBkMEhUuyo3EHvsCt1hh7QPISFfrCzXAgswK3WGFxBnTsphACc+oKFyECiEva+AVnpggsdkzMz444dFA8dX/r/////1onxAeHnCxYTFv+jsjqO7K9WboVDCbpHD0EhRBC5w8qwAAAAAINRlBxVzQqCKBqO5CFOoNf9CY3d6kQ1LQCmNAb6x5Uim1CWRhsQo1d85zulzvPcIBGREmjtJK8pqHI9AQUoBTty+IKdzTrU0soqVs6zYLn4nPf/IMsYFJN/8SjclXSfHG//994o/E7RoESUCJBH1vvWUq/+pNFRUZggYgoQG4vTz9Jbg1//vnyclAAAAAABqfXwyKNJDoUsPgUqeRaacvxTlgCNQXWAHAVCWjNAiDbyBNOXNZFlMfLyR0aeiEp264cFTFaKrcy6nDAVyJeHoQ5Af85R4kwsoyZkmHilD8Jgvo5jY9t50syNnc5vnepyZolDx5xzd+z/P6/////2VULm//uu322zks7yYvqNgKhOJyxQKEEHy2bBQBAUNqqBhCZtWC4ACJbONlsNibdn5TEaYSFBwit7zE7OM6G8naMCbPZZzL3rNAEXL02nZGfTdZxxAz+h68FyhUjZgXhPhHH5dZI0b/xaDixehaIH/xxLULCxEjhGQ8uWEf/kfaf/BQvBo02ofGHesCgWbFYf///GRc5Mfp2ICYT7Q1jv2xGSzE8M1ULYrPIosHkQ7F6FKFN0IVytbk6PTvRtGllMgS7aStlgMdSGR0W9YjsTf2XxfLJz/+7Rk7ARkb0bUU1hLcI6MCr1h57YPzTdZrL0PQeIuK3WGF0mmi1f/VSDowdy1Ud3kgHAJPVWF9jz1E1Zydt2mRRR6Dv0OT//////5FMiK3//t/9lc5yUOcRA4DBIY5WqQgAAAAAAgPlzzGA2oBwZEEOIjQcJYqas6Z+whWBB4EIhqg9j8rCr94z1ZQ6NS1fqa8FtEchL+QP8AACVRoT/ZNyZpKrtx9Rw7Uqa38SfOgll744yx5lxw5FpN/4e8DQwLX/nKaGAGhDdM38Vyg+bnut3SI/9bG+57XRZwNTnQ4PhUaLTEiCcHoLVcmDu+ZCxWX5ClTyoAIAAAAADg+AEzAQZoIyWGiMxG8w1i9b7K0lylGVKRXESMLxETxIggKYPAYZLDqVYVLe4uOpakqkMRIFkC6IqKriIzaPCcUNPfep4dWc39ix7oO5w4K4FgwIzqs7EaAqoQ7cGyIyyudtu4gNhEIjlP8437//////dEm7P/7u3ak/x01HG5EscahISgKkBOcNUY0u6pBJIgZQjEzNJFTpksydI6mtlu0Ubx5FVggRW1ipfkiguYougqUQPKKqiiDJgmyghdDUqo1QxSPJUeOUkR+bzhHzQNUljK9YJu5za/RmT1RAkEQkWf/UYWXQYZUU37NR2RaCAdcacQEoE4+5xQVFwGCmIrCzrZkEkI+vhGlgKfVPJLgEVZ89qYbqNs/JJCjyDtEUjEPbR7JaJDv+sJDrDVV2jgwxI9ubfAkKAErQnFB4mYG8CBI8X/+7Rk8AZko0hUa1hD4JSMCq9lh9IOtRtXrLyvggEvazWWHtFXopEg6UFE4QVh0cgwBoTiYrHhwRSrjcqaV9xuBUZc4xv+n/////Nn9rZ6N//mf5lTsfzROytGg+SJiao8Nl4xhAAAAAAoKofN+zMGHs2BobuH0kPOPU0xOlnwBNEJpQINHPkONSoVc4gehUB3g6ldVdhyGuhqHgB8nr10p1hsP030gQRWCwOHYLpL9XsEiAOkvyjeuH/g08v/1x4SByHY4U//0Ugja8o+HeTfiOFu0xlywwQAaasw4WMuiIdTxOHS1NX/wO4ld6+O09UrDAAAAABAXZUmostq7D3NeI2uTrLxssQmOSiIVSkygp9FEVEQgSTWmCkNjLkJvgBS63OCtAqNlcAuoXGQvlTNGePBtb8XXo11pC7IJs8lzWUin/Z47LaRB8m1ehbbEL8FQmA4Ch5AkE2dNG4eCI0Ufb+Zt//////65hzW+h/dm/70q7td/bJ/r3JUwoXt99GHMpMKM0NoHz4IBgxAO3x2ykVqolbuLsTnFDwAI9MtLyVzqCXwh48B1ADCCiDJFmPtuMQAGD6hF9XDRIcxfXa6JmhLRIkMNznt6wIFYMMvk8rR+IAUUCm/EQ+FBoqE/93MVCRwfOYaKIflIspBj3USEgcRHCwfAw4cUc5BYUQ44OBlvnH23eqPTL/Qw9CEdRqwiAgvyUeRZG+j9YPOa1aEYkynaoejLBhaoHbiRiG4KiLIjx7WhRGQqqpCDzKbhZT/+7Rk7oZkZ0xU6y9D4JHr+q1g7OgRyWFVTLyvgjOwKrWSo9hjAKcVibAvcAGzrWHfU0dKAWVOdSLAxKOX9Y6uMje6ZiC4ITAyhryqYt7WdqXS1+XdlUnmdf9X9AAERo04r/rt//////2YqyHb+M5af5sfz6uChh3Y8OXRVkTQefNpUEEAAAAADqvf0tsq0wNGGnM6wZoYYhsofll8NoC1pyKGIOgC1zdZUkWliOD9bdN8bXX6pZaUD1jsSQDQAHQcG2HdQ2UH4rRJPNf7Gr1/+woYOJGf/7XuRT2RzpkSpI5rzOXjM2//OQGmFYNV2wijCEKTDA8Nyqch3dL/1rTAQAAAAAAAc7oK7XaYgoAk3oZOYFaFeL0ZgzBNBxi+7A0OiRcVhqNp1Os0dV0ShLCy2aXq/X3YUpc5sXl0ueOKx2NszKREWfK9qgwJRUEveQQ2XgZusnWAfJjrfvzOTiBCi2H////////+hwRzF/hf59r2XXnjGIzPMJesQCibIM0eKhmAWLBOKDEUeQgs4+04y/hetDGRAZEAqln3ASob9lEhpIdDDo2XuDoE+JtWw0j7Pchbc0XFUXG+F0XMW4vgpZdYqkUn+eRUbnADw0dX/rLSY1/+aDckTZNWJ//1qqrK9HI13yz9kuOw2fpimudIOEi46s9kbD7g4eOHE4yh5NO0k9CAssJ0ehUAEKqH09k7gPlYjO0+b7FAKoYI6YJKIwtcXfFVhRYMCwcCIBgx7j/mAYDKCCRykqo04LYdSkn/+7Rk34Zj50fXewg1wH+L6t9hgsRQqSFTjL10ghQwKz2HqphU4hTUnFGc0+1a+iq+CLsmkc9SDnALlPDEU54dClJSOjdB8JI8KEi///dE/////3QjRDX/u9Ohhmfsjm0ZSs05bzXZkkk0oSpZIDEAAAAABIURMMskLWBVQk+ZYOlEKyneJQLUUOBiioY3RyGha1GzMGynYFd+o9aMzB1I5JuSl7mkNQZ41ClmX0nt36tEqsXyczJ3YF5/4mg1hWjAAOAt+oiSUb+fLHIjTx39OYX59zh0060E1Uny41HygXcmeQnTfQRUGIKMCeauPb2HIT7e/algBiAAAAABQnJTgosdVOUC8m0IRD3CAyxgAoSmvAEJB0DHOiEBiINRCEJrN2L5qrr3QdUzVGAQEuAFe7qwo6C0FmCm6pU6VJtKYm8MWX1HJb8qpHuZs7VEwpmEy7sErrTJke/FmIIOgWlBsxUt5CSEQ2UZv/3b//////q06lv/8//J/9RQinRbBADQmjmQZJMHB1cM+Jil/R6LAnoZAS1YUDqwtsTOxwa9SHrNtWtChIYbrYzRsNxuRG4nYc65iOmqbVFy5Heh50PGGP/8ZQfCIXmp7pLL9o6JZ4qDmPX9nSbUdHjDyxOujrqqzqM40NVSKGI5MSB85BOD48H56lC/4/fjYuy3dgCgDyqHASgrXqVL5mRGRD6NjbiMFQBDoZYigtMzlj9E0NZbdIGa7BxCO6ytyaT5yDAMcWYZzcu0UnpFuOsHoUBWVX7/+7Rk6gZkS0fU+01OsI8sCq9lQ+gO7T9f7DztieiwK3WXnpis8VaYZD7WTreHSeZpx5RfASeEpAgppjcphGODhl/6///////u1////2TpUybxSXNExs2jqpJ0BAAAAAAELjhBGpywwCXvAQ9mhsdyLpMGTUTeAQscAGeLANagUM1K3c5hv1zIyu6/DuQ+hAkxIQ6KmTfto0/BvWqUrkMkBhRsKMEKXJDtTm/2026gowNUE+5G8PCr2wLv+C9BghEi4w4bX/NR8QpuqpFz11/EIYZZEoAkLsHAKgFqBwGgyRw6BKESi18f/5W2TXY/jMksgAAAAAAaFnBU1Lrp6WFF5SNi0+0iWbrZZKAh5lzwRYDSS7AMAjsMNcWrGEtRGVPGOIPJGTYQmM/MoQGCg6VTRq6xmFOkwlGN5YbQFt0a24WqFy4m8a/7DSaJPGHmVMmdaLNYGUDQFQgIKw1tx4uqANHiJR/Z84z//////oprq//b8xrbmHl06sz9XUd08STJYIWxMSnKwlpR4sllBTLWDotQUBo7N4LFQ2ZAxIwhgtNN1w1kOSgIch6LVYPVvVhYSTCTlgcTuPA4F07Vx8XFhTCh2umCb8ZcKYnIM8git57X5/92eYeJxLXSN6/iVz5+Xvlanm7Eof38dG/FPtSXppElqT1NXhJskhUaiAKCYd53KuH39GgBBQVFQJiAjPqWgh50TiGoLVY75bgRlhkqBRKREYadADDF2LYdqD5ejqGIAcrFRCty1AaCGArsJDL/+7Rk8wZksUzT61hDcJBsCp1rJ24QtR9XrL1tgiowanWkC4g4rALRexoSTqOTSogk7RORF71CqizyAU9IuoozxQ9nSdiy2ZQw6BkioBhKOsbAtXzcEsDikR/4xPr//////3CgZCi//9p+97q3zr0PWAeiAj16jUAAAABpXtyJlr1BqG9VBDJ/gY0pYl2FLkJBdcdAPFmWEVWkjgJrHaCbsStNVPwllXkEaMyG6asD+xAHBGsq1V7N9hYFgmEShZuOPt/YB4PQidBn0OHBwxTljiTas/5k9LEjDSBUfGB/LsQWOj5IHwqYbhOD8l9E8p/ptghAAAAAQE8MlvXodKSI8MoAz0121Xcpyy9GAZKuhoqSSGMSanDjBHvd9VVlE1FgYFp6jSP9iBIyHJGPiQfKmD8uuPf2lPC+OZXMjUeLm49Qxtn1CAYSpl+PoVGguLIZ+ccn//////6OpyEv/5+m1G/zvREmE8qR4AIQ4kYsXuq1p6CEMCTB8lqFycSPaHICmwUfFSAOWBAdTghBwM7vp5pDiooWINJYe9SGDDIu/StwFEvbMrSd2PyK9nBpCERadhvZUzt/b3f/rd2RtMZfz6l78nX5m7/ys4cA0Ogyg96nDqSOytdtexXqv+X0bTF0q3oXHkUZKPGWG7QxSQIxSCwMuKIrhX/i7/69vuo6n0AAZVIDCa9vwCq0QqDMnOrQwRZChohmMoJ0AWVaxgCl/zWURTT6bRHWUQAKiqMvGlIZI4BRYWlWXvCo1E9SuBz/+7Rk5YZj4EfW6w87YHgLmu1hh7QSzT1PjS08ij2wanWXlxAFtoKXa4TXUIKhVHPtrjwEMO5CT6T5pmQWFXF8YstS8+GS9Y9Vib/8MMEDBE45T/1Krf/////7FSQTES/qb6ItHoza8sVKnJEBcdzEDgcdyYiAAAAAJN5IdDikuQZWehGzsPNNcFgSbjvF+QcWYiDUKFvOBHldHQ1UicELYlEpgpkKIWewppe4EqNUW07noh8azIZD1q//yZija2tK7v/anivNitf+ILBMQbW/xf11LtsNHiBe3/30si0P10NDwRZNcMiKjHtNiofmCELCpTTPpZ8XL0a8x4qFICMAAAAAB53QnAqUcZZWbKzEw1UvSiT2mmBBYZfVoQiJRLQpCvcQWyJFtFeM4mhdCABPC7DMCBnbs9kuXBQq2KlX47lyhVrRFk6qppvVifYFh24prS8JQ1FAPRk1yn1EiOhs9mN/7/p/////0VXQkXRvVUvPNH2ZqMe+d0a/Nrn6GDw2JKsGGGR6UCScS/EM0F2WB5RmykEj0wFgkkgSFT5Jhbfo4603Ou1IKBcK2O8OWAUKHhCBjHX0+lfC3kykJBXPTRq91/8OBfVzCUVZ/y1Oaxa2//IHlh7X1fHPs4wWmtWOGP/4xVWiRjE/nh0H5MnHoRSckj4BUHY4G4z/3Eo4mH+7ezBCjfgkimdFBFWcu+KTQla7kt3nx4USBCqA8w9rqpIJMSEaIYyvhYYdAdJVIhIEiWwrsQNWE3ZY8+sDupD/+7Rk5oZkSE9Va09DcoXsCt9h53wQER1XrT0Pif6wKzWWF0hGngZgsZ0pFlPTcPUJFOBwAqemByVGTLjCpXaWZ+fMzOB4Axw4NccZ/7P//////zsdjFHt/ta3p5K+m2Ti7q+xh4xdAAAAAABITUo8NQkAQHEw4hCTomVlMFcJShWAuEFw6aCOTyq2yZmlq2HAGCt7DdLTFgHFZdQs5RBc6Zcp+OfqOwWCVDwRTd/4B5QcCoQkx5MjjIDjIv/2BqDogiImLek21wj8JdEly9/8VMc0bbcQKGNBxUOtosScDUvCxcf/TINZdB/K5oAAAAAABQumWpcgusJg7TKDCtQnNwUHQQgI9Msv4aaDOSEIRhP0hmzpfzfjAhjohgyA56RJYoRaamAy5GdgkQNQVYK9TrTIdCLL+pY90UnSJJSoFeF8r6OxdhZDkQx/AZE8oEJfXb7e/8AXFBAFIrf9P6/////7btb//2bS45VYi5jiGZ0D4sUDUYgIPe+iIEAAAFxXlQRloWLXYlUYILuHYoXhbqulHZUSsBIKJkbzxq0/kOBIiBHmq1YrH50SIbgtsRfYGXX7cgQgItK4Wv///IDwDj5//KGuj3/8CwqIwerL8oPXi0jZCYkOUq/+Xnp3Or+yh4ueNgdAhRPkIE4jKEDPnAeGlmmZYQEjW+axoWDirBuspXeZui7Vg4OJA6VGMlMJi2UrbbEudBNEYtBrfCTTBkSEJqyxGKwJc66i9awcraS8bqQ857IHdIRYNaTU3jD/+7Rk7QBkKkhVa01GAo4MCq1l5bYPiR1brL0Nghmvav2Ul4H11sTivG7Tksjk8BRRTuJZSKqvCsl6PeX9iYTGgKzN/7f/////9FKPapE/9lijG5FHLkJkfVsROwq8cuSwggAAAAAoPpXJ+pPhYQt0GgEDTnxxYNNtOT3SjHA4gFq1NYSPeX6esv5E0FCyYMr9MV5gsEUyfVxokIxi4kwtoGe+H0JiFQEtEeE7dZD+TBBQ5QyCz9igS5gUX/hkVxUqfn3obaLZMY4OhmTb39NSrMcX05R6mbFkGoOpTyQ2HBSjlrif/+HFTKn05IBAAAAAJh8gkEEkLL5Il+1E9ZUNgxY5eNCQpkSoY+j4dCFv2xvvKlqu8mW4LJAUNoyE0isDlutDa1FhlMTsTwfTKdSKOMWc+mdAeWElzuRx3pVJEznUxLjunlEBIChABBcarW0CITQaZf1RPYn/////6mdRpjf/zndVoRrWRi0MQZW1BhTTsqCLqEEN1AxUPA4OLU5UFUfTSIRJGVpwkAGNDBiQAACMIQkTgqBQDau3UEi1xQLTfQnMOUOR0GgJsjF4WmSqyULkdyf7KLBewLjjUwgAjluhjX/mBgJ4EYAwAmLfxIBtFIuHH+pUeMYc/1nqfORC91e5npY2dOnVxljSFCQ4k8JssxLRIHirgD70m4ZgEIxMGHnc2KBpPoTxRONHW4rAw1aCezzq+MSJTFcqrjGEfEmKstT0xNRgeYh1PgaGC5gsS9rKF8M1lcCsFfWpc9r/+7Rk8AZkWVBU601FsIoMCs1h5bQQ/RtOjak6wiSvqz2Vi4k5dRTR1aHdt0YeiFRmO3gdONw+02GZqTlxQcHWJDNXrn8gi0vKUi6v+ZvikY1//////5ThBT/+hquhjXKnZLar2HoUmuOEVfQQAAABIdEJNW9YxgA61Q4A6hk/KWS/BYWim6Bg0IWDc2IsnjFq7HF5luQcUDVf2bvMGBiW6SJW0x1uyRksOW+PHHmZJ/sDsSztDO//iIgAkGwAY0F3/krQgsv/5IAe2ySL//zRJW3VB5dhgz3f8N+nu/O68SnMFRMY7t5x5LSKgSE7WEACzgoNR/Tr0YCAAAAAWE7JEF2Hs1ZfGmcHCAsldBnZixC823AAgSKtKR9R5EAAv019DRrTgLxR8Ega6yUYkmHBIcQ/Gg6oVcdSfhlvFruxEKOIZCq50To1heL50MskNgQ5HZYE+3VJ+9jZga9v+hIWiyL/3Q7c1jXejf////0urJL1p9Damm2sap1KPxsSHy8jaDs5n0GpxJpYGIAIAmX4weXyMYAqOlQ1FSFjMgKSQZY4orA6OiWhFn4jEUrNSnWXwvRJcR4Zd5okjYb0eyv/wquoyZvT616a/+1JFAecd/8pUJf/6g3IFBX//7oWOodYZDhRHmbn+EH/HF31wNei4iB66kOQPCI4EYaaVf8sJXhMwb+y8hpAPsabgwZS33AxBayYKIDlrkVKmmoQHIlwlFnJSriUxKpiyj2sVhTZy8waJusghITrikS/DBeG7Aj/+7Rk6oJkYEjUU1ha8JFMCr1p57YPkTNf7L0Ngdkua3WXnph0a0gT1bwxs7CxSWVUZxRp7rCXT0Yw4mAk8WD6t+OGqRLP/p///////q13/9/3ZV9/nschBDSo4D8rmLSCAAAAAAQsDBIGcPwSlnMAJBAEa7ygcUAkL1Gy9IMMGGVNVBw5U7jtakL4loGGtDbg+0zLC2KdcVzLbvlFPbF+pqjpXFfgHFYek3Xwov3/wmrMtpBdLO//nBoag5O/EBEoov/q6NPZVFLjxdd9DX0s3dn4kFpF25LyrIfcnEoFAWh2BY9QFd4szyfRcQIAAAAAZr1Mw4PEkrnwadw5wJClYVDUtewJTMeQmkAKymgCHCjoLTWIKNvo5JbQLgIZoBRBCRCIT2GBcaAJTVbRua/2uw7D78MxRXWCk+rTLoBpGZ5Ndh2vALqP0taAJGDSouEYXiONRgdJ/JFBFCQi/+jfb/////qNojCOgrEAvUiXImeaYf1Y091P2SflhIFBjOYOCQNxoVej5AlIvCIcZxC1kFD3YQl1zYxE5liKQk0sIRAVPOQkzNUjdc/T9TWTmbWBICceHFdQJ6vYBwQLDcqNRKCcIADjjAt4rFmBqE0W+VL4vFY7+4rqLTlP6sUNnaIYPaqd0X0+c7vNmjeYXwQPMVe7KxVJEXPfT2fDUKYGYAfIBSUKfbLI3RyBY6fTfNKUFqITwoiXdGhldO8kY1FrTlQ7PM3cpORBpPVaD9wSnq/1MhKkysumqw+iHKEQ8pH/+7Rk8IZkX0jUa0dPIJvrmq1rJ24OtR1XrSk3Qb+t672WCtFj5KqFhYW+HS9o6ZGKgc4EpVN9TtN////////+joYlP//olqddyzI0woI8ypWQAAAAAAF13FgAT4UXa2AjhOY7CxS/JglNdYxKFBYMEBMG4GgGmg1xcr/TCThcAEGDTZIPCUGRQp82RyoSHYex9RpmdLC908fVQZ6lWtZVDJ+pD//plrD24tdY9BF7/EM28kiRl//JmD42CcQCD//5pzOvTti6Enf/PfwYm0szRAE8hzWF0V1VYRNDw7Tchlmt////lKVImEW4LPiAAAAAAAABimJcN9G4NjU2WFOEVEMWCA4UStGhUKh5gTGZs5CMB0wWcOyBwbtI1xBfZ2lEUZmhmmCL2GyEBBBAGDQGasEaE9heFsDaJgrELutaFAi1jXZVCbuaTCkc3XQtaskIhQBRWTZroAWBbCqEIzEYkAKkrRfi2whwoxtb06t/////5xybIea7qRt/+z6XYx+/nUc+egvRT6HziE/WBttTI2CJNaQJDTeVBPH7I0ooGQCMKWKweQlBqnn8hiMQipJqBu6g0sdiMxh2aCKWGAO7EJFUv/SbisIVVbnQSCZ//oN3CUBoBgp5VucZ/JFgfEhOKCH97T6llMFhxe3rpjnzvpqpsot60cUM+n9yg39IcRp+XU81rsFACsrQ0dB7LTmSs940H1esAZ6LBKwjkbEy/iw5pTfV2WTXQ0shKB2cnBwCTCfQsRKyIrdaXLIBQLb/+7Rk94Zk3E5S03lbcJ+MCm1vKm4POR9ZrJ2awfeuqqmcHbkvWnHYfzEt3EXlrT91gDay2Sq3uIxVcErYq0yOyNBOGx0bj7X0xkcHQ0yFv9f//////pKn56N//60p092VDbqry3FBMgAAtjRQLKmTvS+HhMAAh5CeECKICVbAgETFAYVQ0DLhapqzKUNmLy5U4jC0PjBhF1E93VlCCr3L0biWrZhTO8sqj049IpAZE0jnEbDTN5P/v8n1XfBaKLuO93/KjtGLBD/gSJi0UBsZ/igsVcyo2JodM/60hZg6oLmYikxbtRR1IyyjGAKLKC6ODn+TfHrkoiAAAAAACwtDocrNsMdpljXT40LlvogalSvFHYLFiW4iVGpUGAFC1xOZWloAMIa0m2o9TAUhywMovZiReaG0INIDsf5IDYQxIhnrBPV7KOq6dqpclCMtyaIp1qlQocLjQPDAPBTb6khsWFAgHV/9v//////OU9Jxev/q19nPssibq6Dh7KhzFyrvq6ia4QFQAgSLcBDGuMhqWBHgFinGE9gdSDh09H7gZ6EZysQh8plNEgH4dCZOedh8JQt7MdA8VXeZv/1t8JAxpdUuKNd//yUVkrdN/5vinb//5Dq2Fjf/9xYWt+7FG+SH/44oanM9IKSVX26M6QpRwgA6JBOr/qCqDZv1rmFABRR5KwkYBQDBKQ5IS6cG7rWWqu+LoAVroBQUHmoeQhtNguPpn4rGXLOvG0lBM/b+qOOSIRYswncSIkqyXlXI9DT/+7Rk7ARkekjTE2dPIIyMCp1l57QPISFd7L0Nwf6vqz2XntHsIw25hMp+Pk1K9lLhQcpelZZuJFgVEoJDDhj8iQMELki/9Nv//////W883///9GTWh7sVIFTpA0XUsPKVkIQAAAAAGATUorxIBAR0xJGVeYP/DCAMwcJCoGtswIAQ1MGNQwZZsvhOJKmA2HrCjQEomnQs+efFW8vOskuelMYaPIlU0MtVk+O1sM/GS5l5UD3OgK021jv5xmwpUvRdsHa/zEnZgmNmc3/+KCwaklP//gxco1WVdNWX2ov/MXGH0E0TSi4U0Ulgz1RSmyUYNJWTkyxZoj/ZT+voQFEQAAAAEKnNOpjuIdVYdA4YQkQCOki6i1BfFtWDSKMIlqzq3jrEOHROLg4oSDFRKuVQ4iuKNcLybKZXmqe8U3IJbzWbCasasveimgnXGiPDeUjgqGO9h5hyAadPX5wRAGAoQLv/Qme3//////uxB7f/+y5s3QxnXMLVZDlnGO7Ho5GIggEKCwSYMJMDQ/XcIgprRwpS9y5AUBNzDg8KhwoNodgsA2xgFcNh1ShqpjgjoW04D7PxCjiM0iybPlVLbylyTwDUHMdLRo0luknlQtXk/WDhlifz8HWCQj//5QgEDxS//36oz0QhJ7j0q0vZRlVeOMvWlHCzlua1yIoQnGAAz+tk1RECAAAAAFB8C7CaZelx3XbsuQyK01gcEjk0ktgoaYQQKPAhBdsVOUOT5mGRx9pSPrmI6F9UzwglxWSPTJH/+7Rk74Yk2EdS42tPIIQMCt9t53wQbRtTrb0TAhMvqz2XltCGLiGN2MZhhkgkF0SjAqMqxUvmB1ZnQ5zZDiU6Nb4KxosDCxRwo/uA4wNKb/nVv/////9uJpRv/1dDXl8z5NxrVVRocKLHLUYqkAQAAAAAKBhb4rCAgKh6h+UEiYEfBcTMFCFYWjl/ACMIQKJ6AeTLob+U0juOGJBUmaO02SrGXLaCiBIXb3dwp/qtWbUKA3HVDT8lMdcqHfqxp+F40EqeCv/+g0UCvt1y4ZE6sv/+lJY7LUVYrJ6CTkve3P7ceylb639udn7/UguzWiih9gu5/09KlsAQAAAADgeMgz7ZRUowiG/iZu2BiTksXi7giAFQRVAFECRRMWiA/MDLeh9IZY7OVykBKh6wbDtpIoI3WcuFMrac/L9SqA2lpGQ3DcNTTYorDFXGo8jVYRi6zTHbfMJEHQchM5Ibl/KRFKAsUsf7cg/592T///+tNJ6Xb//T+hBlwl+NT4qUCdSXrkXUQpce8RREbUvotNh7OjhhDgWAQxHH+cJQFi1eu31ud1J48tWHa2D1RuhxqvS0JvuTV7Df155oisNPJ+5fWv4iLAKGAOJD/5ir94WKgMLL+hkMNUrGUgicrdbX38nhXIYifIQRsKKE1q4rUkLYs9Em/4TDSVyshBJAfXauKAFboIcZ5zs9IZ1G7OOzlpKBBZSi1krFJFa3IcLCQnMQ5VQE0V6hJkXs9G5tRkZcsHfQJizruHfGlaomOMwMKGH/+7Rk6YZkUkdU60VPAIwL6r1k6OgOrSFdrJU6wbUvq7WHiilwQxlVdxijChtn/MBFJ+3f//////+j7N//9X7URma4bRuwZOYCJ+gAAAQoHDgGroRhRggOl6v0460AIK1UhBYSPAooFCRIJbgY5hyard4zpYih4mEuhsalicwjAUPU2ZGUCKBOnFV8rjUJjGMpRXAKKeil7RNvpI+f/sCgN+WIoiOFPf//9oRchPf/mZCkGgctSMv/6Xg5vYsddFJHX+e/kN6RxvRPdRM0gbRhs0KCCEIgSGxXHo5gQN/tZ+25gIAAAAByTzYZApqkazhb0fOtCG04C0qjzpsPScCg0UW6NJIBFou8weHm4kwLho3q6mm+Ugv4sBsLn/l6izh00Zj8DTTX5E4t6bjj6PtDrts4ciKPKxaCW8kViyaRU59y//IvMDYlo5y/6tkxGfVW////f+hKmCg7//79z3efW6jq8YodIWkOoEQABEhYAH2WCBgAwkqhKyDNYVECGS7TxLscAswLeIlMOVggfO5HRCVNZPR/YXm0ZrjSZ0LgAIqSQaiMtehmcFKZjozUJfLo1F8VufyUmIApsCGbX//qnmmX8WrBQO17UFP5penQ06ctZ6RgvxXxDre49kt25NPLpck9BU2dZ46UHBqTQECrH60uY/yCzAAANR3QtTqHBKOL5Up7DYGHBCYaTM5l4cTAggMYDakhw6wQFXa4hAp3gN5nBfYIdkouCRrvW2jYXMeOQNuOGTOrNfQCqZii2rL/+7Rk+wZkuEdSs3lLcIjL6s1lZeIRfSFRreFrwjstqjWsKbmiaW5E83FtLKKr/IVK9bC4amj/P2zRrwUAWx6CCKVPKEHxocQEA/PO+Yr0bb/////9iU+pATP//7ardlPc1+/yMyF1ckp1AgAAAAAo2EoJYVd6u3jTAdEGQEr2rK0xJhwIKIyEGQwySXEEzcMYU8pEIOFBWLojlMpmUGCJeKi5tN22MU5YVJNDy6CW//A8FADjgMr//MlEX61D4YNCc9T475unSJ5caeNKXjmhlV9D6S00gcqjMyzjxg0aHJ54bB5Q9OH///+mXYkUOqVQEAAAAATE6y1uR8Ri21jSg/yF8lx3ZCgK8zFFDCF4g4NN4FWhdNA6LK5ecCgJOMmpXwZ6PDsMifo/sEWCoB4jcP5RmoKEgIGoqVTCQw2pWMvSXEXFoVaFGyO9jRrlOqU690/dvmTX/wYPiQcFxAv7et/////+26IzC1W/+RXIjVdrxgeTZD9qCQcGuyOGGDbiCjqCQ6z4bQpXyhLjxgrKey7VrxZrZcwE2UvWrHV4rLef2CNAZqnyXrr327Srdxra55fKIJaDRfxwXEFDJ6tJefcIk3eciKweCsCNb/YyG1C7vaassbzI3s+/U/4UOx6mbS50TfKdb/ZtPQjnlUCltwmgaSsSzBc3LUSAJErr//v/2IriVYib/rcQBHEgiCsTa2u6IKPykHkAwsyhfLM6YKgwQLPzYcYUKGIALDN1FlSsDMRlMYFJwtiSiyn5clf/+7Rk64ZkNE/V609DYJBMCr1l5bYROT1VTWFrwiOvqrWsHbiFwpsS+QwHTcgJ2m4UDWWvya/I3/auu6QRtBCwhrUPQK8VZ46QsCoBYZEkmMA9B3+IXPFw7/ntO/////7a2ZjWRP+r9HMMYyeY/+9NOYKjnqxdFTmGggAAAC1QiC/QgNaWXkZTGzP2XajejBHFD2fGIog66rgr6uU1MyN6S6Sli9qK/ccz9t2f6ESqpBfPoYKjK8H2fqXfatf+IoViSr+gwg+w+SN+OjopYx2/Q1bTkaODVBsQZV01rpw27IE3LQ7kmfCKQsZQMiIzBvdzA1J6BQAAAACBmRkbOzguGy5ckWOsFnjkp3I9rwQ/AwYsI27Tk20i0fWA7kWScDOjQ1ZuBsJBRK4BFOwrGqEWKM2mswmUfiAcHGdcSqxnbYw5Vp0d9tq5zgjBN0A7qQQ+MBQOCCws/6lT/////9/KqUf/q/6q9Xt7vy15lGl0REFCBgABC6ijU4yhPYSBiSYp4MqLRIADA7FzFFTGCjFGisI3eItPflWJ8QuAQ9EZg0ZNYaN1BkKqFnat7XwSPeVSJwuW8opFB7AWxGySFZU/b//JREWci8V+P/lgiLiCSBEZ/+NCMBoEzEr/3KWT6/jEJB0KLVfx5JBa06wJw/FJchyDT7JBeaeDcCygzzORrUyW/ofgFAAK5fLdUqHRLFnCl7XT45TVGtH1EBkSwYiCBRYAqFMR4NAxhYUWQ8CkYDMNUBmNoeJ0EgBRNB/JZFL/+7Rk5IJD30dWaydOsH6sCt1l5YoSQR1PTT0Wgg2wK3WHqbhU32yGcZPjuNCO5Vo8it2AjwratVGpDI2hEsPhZIyciFZm8oMyEOEglN+rI/6nn////+m6JMOb//6bNS39LzKkJIRLdB6KyqRAAAABQfeYiAKHIZo/MEBoM+boUBK5T4h2UmJRBQcELHFSSaSlelxZSQUrEiKAJXKsSmINIv+01VOAAcBaG9Uh3zlLKUx01SEKu2U/Ku//hgOwTAksH//ROrORWn/8xPDyAUqULf/Lu37PYm5VMmuRpnw/mKbLGfZIi7GQo2y6aIYaoymjDBIUZ7Sofnf660BQAAAAHQ+Shrqmogtd4sjflDgsUvn6hkgRJUUj13I7w2igHLP0hu/qDocKwBVBurjF8KidJdkdDe2zcriaoa9UpJG9mQ1VRnK8JwnURMLHFdgKVesynFBiAxPU1flBaDECcZjEt+pqHfRbf////tqaYyp//+v9vY91c+cQuxdlUWypNWwEUXhkWhNT0TfHghdFyzvFUjYaYyspGcRkYUVii/q/gQEdRptVWNYBIdwF0rNpWEqfeG2yZM5zo9T6r/9DURebvDzn0Mv3/42LhGF8LYtfUbIVcz9RGFBohENP+ZPPTx8w/Q9oxjX/27mR9xtE4msCkskwkwo6ykCZAH0HG+uxbPz16bAAwgqYxS5Hvch8FhJEYniKKHVOkCDwYCAB1tEMRPKROWVWJjz8IIIuMCrZC4rBVsgBdC1gaRKuGp3doSf/+7Rk6oZkekdUU0tOsIRsCs1l6rQQjR9VrSjaggMwKrWXltirGsuCnVL8Uk3XLCATKIWnp/iRELIphZzfGGeDZtodl3T7DvO6f/q4EBxYR///b/////pRjIb/9u1W/+cj3yCz6ZBYSjQCgAAAAnoCAwGDghUoXCh4aUpA7WmEXhAQRXBxGYcJGAi4fhTpe40pgECNHUsA2U9GXI5K9gZLwmk+0nQNaU1d9089vdnnBqwwgw8DAn/iEOt/3/xlq72vLoWlZ5//piQKh9oh///siIAIi6KD/+nfojk/LxGhWomlmtf/P1E3X/FogeQrWeZTpLG0mjxIGY2ARPrcKn5n/S4AAAAAAAOBQcCCAMeYg47IRwAVKZNLCEBQCSXMEAIiQMFmbEpwBYUbQCOBVxxxK1QYlAuIngn+BAIgUlm42z0qiVssMZsGySZNFxiFwWgnQyEBAH8I6ZZomOwhuD/MpFBemGprshf2U/B1RlUq2DssfETA6AscKDDv/Kf00O/////UpR5hv/+n191dbM1mYw8YU+isK2KrBgJAIACZvL5lmw44QlMJLqNgPoBTVi6uarzL0GSxen2hAnJJJqqGyHHmhUCobRH5huxY3cqGeJqeDkZDpcqGCwuX/xM3Kwmqd///NKmz6/+gEVFqpDf+PZ2b9hILSc9T134z5eHwsNg9fkf3BQuYJQsU4Oo5/WMEh6/18wsIAqgb2Oo4JqytsqRUwFbSpbKJjdmINu+okNVFRkRARbWq2SLvc87ptNX/+7Rk7AJky0fTY3hLcJcMCo1p57YPoR9Z7L0NweawK72GFtA9ImWqmbaRMQgKwfFmISFB4hpBOHRJutDFl5EkOlhcPTpdChUExcBgAEin0TuGGAUVu36f//////ozjjIQr/+jXKWi/6M4xpDKU44Zz0cUlYbAAAAASEpeUHPhGDC4Quq1l1jipW4JlqyI7p3qzgAmElNouIfSdWNk2MU2jgdqGMIouLsJogfDjRZYUjVqc90Thgm6hWG5z/+HJDxoG0ksf/4aFWR3/qIDiwVRx3/EbX1+tJNzUtXzxY1nmXUebcW48abaj1RQiMoGoNjfctXf2r6LkAAAAAADA+Kki8qVhb97FrrAGmkjxNMxRlAYYQIiGYEQClCU2dFWLlJzyoigzdVJAc3dbxgAGAZi36ma0wIVS9U0iViShaPTxSCl5ZNQim5Y5c6ySG32WcwdDhH03X6YdKLIiCsDAemoJjBZ9BGPLDQoV/9v//////nllUfZ/7fRJ1WuqbEix5NkqhgLAdjtGAblUGCC47wLWTakBpguK9EALvG4sHMqPwLTOohNL8sHq0l2/OYv4oekXeeHkrEheoHoPgSRGuLsj8BiAW9eoM/82UJR0ezf/+Wy7n/uxvXJx9h18z8T34/Rx1pOru+ekPjVHhnZwEImd56JTUKJwQBFUmkb1NsR/9NS4KaavHCjzAVSS3BwAcg18zwkHk6FC2sSh5ggJ9LKxrXQ8iyfp9mUC4L8RgqhkjOQ0hAm4vk++RTmxPLSQ1P/+7Rk5oZkHEfV609DcJNriq1rB25O4R9d7KzTgc+wK/2XlfAqXXhXVl1i6KhJJaPxWa1ZRAwHF1Og78aNCYmrf/T//////pK9W/36vL1XXqrZPRApX3iESvBgAAAAIeEQFCS/AVCJrIT0QDe8wCBRzYk2pa0yxcEDRKSdC6UGRo7O+wGFhmjVDMRuVko0B6nO42F6QVMu1fyg12MK65heCp5+/KIVr/+khmkepkka7//iCFzhoWEb5gfJnIUuHi/4vg9j0JURRM19xfY5JWBoiRO0mCoupStRzRDISBwehosOp/bmJviB5AgsK5b5Uj6gAAAAAAADTEgChUgGaKjiku0I9SMSElxQwO6I0KEiwhJLeDAYqIMAwBUQwgp2EJSdahwhqmMLnNLQMdIpcUoQFGwQ9J1GWojkS5wiDFLr9mRr/SalvuBCJ6CoYVSXmyltks1cQ6/teA5qWwYn3TV6tn///UXA7OEY1/stLOv/////9kcwuqt6bP1eei1M6nuQbZ7+OikXbyRdoICAQAASVzzj5ACIQrWQia0AEVK1UbJXUOEAlAD4RTipXFFNjfOdYAlQ9zZJVUrmxvchirciEa8rDluHIPxVL2oU//i4UOCIMHf/4cj5e/mLwPNFhgibX/F5Fp18zK38VxrCRQ9jJLUszzmEw/N3VxfEIJwUP/A7KpiJRRKpaXQDJhTgjIPsyZrLbshiwHkwp/XRb6RrSQwj63FocYDLpZDERaAwxirkpiqasFa7Ab8ROdEwylj/+7Rk84Jks07UU1hDcJpr6o1rB4xP2Stb7L0LwcgwK/2EntBZhkKhUCBEy0wTuFCNCsJGzgKsIEFoVIKPDccT+NSahGNlf+///////z3q5c1/+36Us1Fb/+gsO3mR6qkwRBAAAABNuYcbNFEQAGEFLCoC0wclAADTlxs2jTSkDhfI6yQV6JupA1Ahx3o+HB0q8JxWICryDnHeXbCMHGfsFkif/8Ze2Ou///8iSCDW/7z8hYbIWUe//yvvjuPvLQw+//+e2pD1CMergMmkk9aOrrNwea1QPMExtQ6ptHt1WAAAAAAADgNLYHALsMwVwhCuUXARIKR5C4CrXPKUAYMUfBBKr0GDPChHVk6gJrAxElqdgDImegB6ayX7ahcSBNXMLVrWrLmCN9Da816Bdit8KkN5drJW8UscdWdpaOTTXGkCwzKoo+kBXVg2EOvNyzLL//UmLwdhg9n/rNZP/////9TSB4CMxPr2MNJmfqCN5cT3EMgAAAAFGUKBIAE+ioEuos0gFOfwREgAAoAhpW1O4mIDIwgRnDeGKTCNKI+Xo5BYG5wKAugyjjRZ07R81zLytSmkEbEPKhRMkt/r0SUP47ACyP/+07BllnzXkVQ3qzS//mWRam2lXFs3+hN3SMQyafyoYPLtbOOL2pGxokXjy0+TTF1ahOwpcLiUvqf9uZAAVABkM4LcETJKCBx+27G1xl+U4wqEBJkxcQySM84MwoEyDhBYZA6ky5zGEhzNIJ0EL4EB8BoFtfDci7yF8Bz/+7Rk8IBkAUfXey9LYJJIyn1vB34RwSlVrL1vQkOuKa2snfg5g6duPN9VrACBnaiFHKmvNXUcAzCZKW7M2IIrI0xhH1FJ3mHQzRPehxbVqMpjkH7//2A8gBYH5I0o/6kv//////jsVIfKv6fb+1/r/+SO5Kq4igAAAAEsOiFADToHgoFS5NdnhyWl5yUJrcjTfRdQ6JXsRbDdrSaUq6f1MouSRCU3ZdRySLRyna5LMNU3y2Z6VR3Va3Z+MSjn8WRDjQA4d/yiqT/tEFBKjUrf//dOy9RpeKjZyvfrIbNudQ2/61OHn2rkhuSUD7IU5Qo1t9u99kAAAxQMjLRoIS1QvOEyamW5DAIkASmcwZFCYGingiIY6QHiaMJVZ2icalJil54LNUhgwhOUDYIOCLMqqtcbVgMTdZR1rKFzhMMse8MfWUTHSaWyjopWpUnC+KoWbOhHCQE2KYWInJ48sgeslCmVDmWTyz+db//////6ZkwLhH/7f8x0I5hIABgAAAJDqqgClF4RgeYkkLFC0p0zBgRJadoDWV9jw0qGC3caWwlssdgsZUQrtBYsymtXxYjjViKqaoc43TZayj2KKCcrJbeo3BefdDxFAELK/Rlo6/oPEAEUERUav+GqJe1ZCKpKnn6amTL9hp5cisq2kwODoVUQDhKBR/+1zg5GQAARCGMkHeZNItnB4EBHDnhBYWKAQcgAKgYwpBLM2iAWNC0IAFWopso+NPSOBSEazKIteVLCqSBbrNyC5w2wFW2yZQb/+7Rk5YBkAUfV6ypOkIMIqoVrDW4QYR1V7R0aQiskKfGsNfA9djLlLn1pkJrrFzd/H4AljAX+ZiQMV0wZgMNL7W8PIkgXwTkJOJyPA0JpRS+VDtQKpszfpf//////oJ6SSB//yv+sflAJrQAAAAAAcikEEaoRQJXaGHEMHLCIsOuULAyOzch0OCxomwiElCvMmLT7aMBCQuIXSApyIsCTmZMdEg4QQAGyw1Gbaxe/8HrdARxIPrutZv9DD31aa5UqKwsOQkp9wN/tr16gXvr45nMnEgmimpadeaZ6Zmb91a2u5s+t6q+9J9zc/X1tr3auTVULxblt9e6ykHSVRoqrE8+c6xKohdZUAEAAAAAdabgRxuCwbD15ASY1oiAsNgd/SAGWdMYGCB5E4Cq4HSDGBEJQGHQ0XyNKWBTsED3RBok6SLvGUpCE7WKLs7Q1GAFuskol/NQERFY45R/ZYpAMjUxXaWXZIxF9hGRhjGXMgh/qTjIHrrR+pO//OePi0DAkHSJ5NnbUt//////9TXRXu///tW6ffqv5Gf4orNkCko9wQWZbhwuABl5iY2sTrEQKOjEIPwnxgR4XagKYkc/Pu9CWdpvzXL92pchp62azqBX/eAJguBF8ahTjs8SCU4Khavm0kZrf9+WJDgFJPVH/+OILjnPF70R7/+ctz8+jUvTRr0ouqQVC7Nrk4xdV+7ToKALfCkAgQbyARpC9sFPSyyGhzawEaZAza8ykueTATfS3YXNSBvmOULR1fLVVTX7/+7Rk6wZk8UfTY3ljcJSLinxrB6hO6Sld7KE3QcwwK72GHtA5KsN12lY33tQAuXE+KolALD0gbMEZ402yNicS0xCMV1HxvPDAjIOP1zR4cGZWdf3///////vRkLKzU/7Jpbv/b9C6F+kcIBQAAAAAAARPkiwWWS1QSMOfg8xhcEEIB3WRUfgCBAWRHVeLNlLRYkWFgNVLoAyTc5yW1cJhjTBE43bpKPn/hAr/jjWVsFuR2W9mp7eocaJK38hyb7/wdZR0jzvmvKCaw9oxKM/5mLG3UUWWosyxf//D48dNjA6Ga3Y1x+ovDighgIlCCQL39/8J+a6yAo5P6UgwEAAAAAAIC9Q8SMQFXauZRiQgWzTFzBAUq3RgIhC6xZx2FLVBCKTtF83Th8Iq1WbVG8QtZfy3KA7keerOFoUSGOJytpbyZKBk+LolEqqMTgSR+sl/OiSHQHLmmCSidSjy7jQJY2e6t1RG//////9GPKkTjDn/16nXrvt9Ez1dxolp7uUN8IlIACQnShFgo0Ed5B68/x00paoINAEgYIahKTmEgwsAW/A7GW4KjfxdayC8KcaoIpacCcsS9ZKdC7u56/kbcOENWS9XLjEoa5//qnjDIq1u7F//xxCgTfwRkI+tqtJ/+fpJPdhia7bV763P73+sUr3ahmdQyqTRRUqJGmbbkjEgLTt4fiCl76OkAQQqCBtBxrD6rgqG0kpbsyTCR6DhrATEI0PRKL7IdDDsqkqgwhcdegBQELJjvYloPmbqQ0T/+7Rk6oJkgE/U61hDcIYMCs9h56YRGR9VrQk8Ah8wKnWsKbhkMBYcdmCkaXddB0X6YS6awrqQ7/ZK7MNxWC3KdRDphFV9RSk4RoI4FxGKj3yB5g9LCYcphjfzD//////mOaqnTLHL/6NzeYjuu32zufkmZJjKaDAwEAAAAAWbSUoS5GCEW4sBjpMfVyhKsTEcVFRQBG8SBhxscMQNNSlsDyLxU0beOSlpTiXm7kRKk4fTfOEVIuNYGkYkUPGJi3pl0ipHl8nC586T6Jt/1YA1Sdt/3cU9v2OJEg74f+b5aFN5JGCOIJ8TD8QRfLg0NLFQZHf/6ZJlh33XuQAAAAAAACwqOrY8TIqB9YydsTTXcCAGCusscsqjkEFCgCaapWmPkhJTrX4YBLUlG6AyjlEWnEJA4eptOrlINZYmw9Togm8aKMtvKLOReo4PDweubEhZNlplPOLgGh3ULnHL/s5yRK303gd///+SBdYj+6/Tv1AStaxBYwgAABOLvGJThw9hzQgaKLZHf5mBAsTByqQ2AuQgeDkgpE1DhiHGYNfgiqg+sxwm6QSXtf+KrsTCUOY9XjECfBDHHlS/SqUCbDDszc///KDgOGRWRhv//qwEYMTz//0QCILM8Gd//uUl+wndtml0MGf18/v/zgjSS3sDGLgmSw+yylWCtlCYHScfkvWqk2QYRvgABD4oJDCA0ISWJACqTXTlKUWFUC/6/XuIQrgqDgIcjIFQJjRS5F0RxGKVJCIIWTAoul8QBGyF5WH/+7Rk5QJkIE1WezBFsnrlar1l7LQSHSFPjWErwj2vqrWnnxAFrX4hDcXLKAsFKjVhkijOQqrXUdxzl/Zh3Q0YcCFN4tAhpbFh7MxKJCoy3atN7+HEQahtmMR/1e3//////PaTJjq/+vq+p6ujzzmXH6HKzIIg13LU1dGIAAAAACTMgWAj0qRecUrJvuZaMFQ7EWCyn0aCoFZosO40of+BI6ydfpchet6Yxr0N6fzTBeffYH+DNQG2rLePK4OUusc/KKFGSgDBt+jqxn48C6Gw/aRf5rESbHobfna+4bLLj4vamrsFSfWYxKKky1j4OO/pkbK76CgAAAAEA+oZL0vC15IAw3I9wFEFoJhLDNDdaPq1CSKb6mjnjwyfSRDNy7yK6FClzhXUkXJdh1AaG8y7LE3pg/C/IMd6G1XLvKxGV76Guj4KFjoT8sCF0cFqitiN1bb9v/x6ACCEFxv+jr//////7OzqOHD//66e7vUp6mLjWPQPh1isjqgAEHSwRBTNBEW/BQUrOvQYmuuxShYdtyUELEyEengsMgSWQ4cRukwBlQchQPj6DDEWvvngwSGEcmvW8HU+ArqqltkKeLztihqOsT/v3JZH2byh2sP//iw5/oHQ+BQkOl/xYjGqNIEgKH1q9vqxlkLyJEqqspuiNppamGKHALXPFHM9w6Np1QggAol8cWHlK6GKjVMwA7AUODF0zFvsxSZlBcYDFl2h0EeEVhfVLt6X1CKkz0fH6Ch5MzGJavJAeJbGMz2A9lH/+7Rk4wZjzEhV60pOsIUrqs1l5bYQ6SFTrRU8ggYvqz2XnpkZK6Yi7qJw7mWzWXJeTarR70qUQY8Sc0WDYMIVPOftGBWNy5E47/Hz1//////89xWXkCj//V2M7+31U6xnZSPUhIqGIAAAAAAAAQMEC03ZxYxUMoIw5M6wJ1DwZbK6GBCAAqwhPkIBVqqK8FjN0ehh60jHiR7G/KaaWqmUDRxo5bdMVh9ukefv0LSYuQi4CToz7Ded/CUAmGYiATEO3+q/yIhFUWz0T+pUszMo+NIxNJHla/0mzH3iRK48qgzV3I5I3kSQgJjrKrtBQhJd8OQAAAAAAACwsZZBpjqjJAWqNfWML3LNU88yTJZtzwoMBk04DOAMAsmITfupbM4BgrKC4aHiQ4MLTGX4AjhQIIBaYZxyC6HLAIUtPEkBpVc7n4ZyRF87O4si7p2ImCWphkcl1HV6HqSHS0//m5MawWi1/+Op/b/////e4/ec/9KPndv/xzvaUN9TixpkABIgW2UBWJo+iwFNaATITU3kLxYVAqGQVMmXClti6cTZJAzTeMPgsHGxZ0Xbm4sFwT6zEfL4gJgtqH5M/Nv6GDnnGBrKVAaP3MtRuX1htDmCLiNBxf8wNPU8uxsGkymc/7OWLk/j1Mi51qS+hid3t5oqRoTidzXTy7Jg8NKPAwlNuPrP24IV6+sYqFNDAAIF9roK0MBAAAaBRGUkWVA4DBoYg3ELEToRzF4lunFSxAQnca63JhZhPWWOXZAAlpMxYmv/+7Rk7QZkW0fUe0pOsIuMCq9l57YRmTdRrTU6yf0tKz2HltmQEFfJ8olWhMCVlPoqRSi908sJgVyiRQnSIHHHQw0mSmYzWdzG45tq1/9cOD0AQBv/l///////MLIVf9L//Jq/RjsSIqRo/PJP5AAAAAAACF4OFFYIZWQkOyWjM1ho6GqKDVktF7IlBh6OjTWvsIdvrLC+IKGEhHVeV6WMsluOw4kPpLxlnC9Mv0/L0kAT+sqtZQ3RwbLK2GOCsCTD6U/5Z9hIIu73A/H2IgNmxkX/xOmt6WKkH3/X9PBcc8ZFqaKVJAisPdTR74eB4Hgw2OK82r75yLyC1J5UwEAAAAAAsC9SoRwtbRSUxUuqKTWEWsme7kDswUqaCAl0hkxAYGzVY7U22UzGuCZfrIihwoA0xbhZmmdiMNUqC8eo/T3cY+ds6krdOKZxPFnNJgNzFWxVt6qjv3F/D16fjcQgeJx3/1f//////6OXQeO/2Y75ruhpzVV0OdnM3RXoTfOOIjg7Kg4QgAAI47nqSxS9ZxDaIq7giJEJuKWq41Hwg7V1Ju7IWuo9sOl1G8LtNLzj8/Sh4SeH8GBCVWBP+LVDYEwurKLr+SpIzYZr/4htM0Uz7Ci4dNElGi1RsX/w163ETTUzr7//74emlbYkR0xnWIYAELvZ4Ua5r3fmlPpliAiEAAAAA+5yqNCVAbfR+SO2WcUwglajSlEi4iZDOaC5Pl2IZo3EvrEak0BQeAGIN1Y9DzpOrE4LiYOooA5MfBj/+7Rk6YAEdlBU6y1GgogsCt9l55oPTR1drCzVgd2wK/2Eitgs/slSAEjAwGhQubLDtQc1FgfP3Hyl9/ABIxGN/w7/q3/////ViOn//+na1zKd2znoyIvuLCJQgAAAAAA6dgKLHTVBUX5ehkc9igbptkZM2MAqBUosAIT7iNjkooPoz4Cglvw6KsXiiyIKDzrR9L8IJYnpj0BT/73KAiBfrEYbppLru/ypXcLzLrkkLl3/iEMlSw1QeO+Li5QJz2/uRNoiK46Qd/WlTLpYpKqtg0ISNeUDbsouWQRIXmH/9tyf0O0AoAAAAJh+qogtFWttW2aOF0sdXqmsxNJARBVeFxHYETa4oGx1bqbL0OKIyrYnUQEx0ADGPkWRGibVXgkKChP0JkDNDkY43UyLSJyszELWS0txjpOdQrby7nGIc5+14OPjemSOyMDRFxj/03801oT/////8mNYbX//3utGUaV0lJNOxxIBhcJAByAILr4AxS3wcshqNCswQAI7ncSXGZcz1fbWtJoAZYBBLHdNtGI0iJoXJNsEFDOe29h4UME48VYBQ1FuIkQFy/vUlU5IAi26xG6Wpd39ftwrUSdBm9mz/46RFohU1fjgmJODoY/0FxTGY43njG2f+Tby37fbeTlky9LIJLGFwmCkAsUSJkGfoEF6IcQAAAAAoLgyAIGlGXWlz1LChYyYcSLWKpMhaaoAIAgkrvJKNcQ8YQXMnGpIPLIViXWmeBGiU1qLMAS3TZ4+Tez0NO5TqNKdOa7/+7Rk8wYkR0bT4ydPII2MCr1h5aoQvR1PLJzcQjav6r2GF1BnP5Dcsd4GZXBgu0Hz4UBESVK4Ti4BwwceWKPnPgYLzqbV18mZ+1MZvqv/////73LM3//Xf1U5HHTFONPUOqMgKM1jzdQAAAABAmRBOo4CSVTjSvgQX0hq46wTLUxD14YArenynQ8rCUfnWTPLygpD7tadfrIEqoM6mGggGrUDc8v3LJtRUMmCjtctUsj//8PMksUANV/+gOtI3QX/1CQPzFR3Fts98tuD5T/0VYpUR/8N/DmrI1QcF+9mFymHoRuAYVDoOTe///0TZiIJu9/wgAAABILqPK8elxG6r5YUg25aaZbNDs1kFXZKouJGMIENhGwKHYGtlxJWuxaTLy7ir0qnHYQXuBTX8ThVBJhMD+ssokP5WJR/u7caZPj6QJuvG4sJ/wy7KHCtX2IdC+qrR8/7/CAfMofciNlMcx+v/////9rByzv//0vvRZStYWILOiUGlHrd6zHAwkFU7y6TrIGkw0ErRhbEyh+kC8pegi0SCCEvqyAaQylRMN0XwGiGgmSxaO4l6pgE0EAL+9T2NYTS5MFFFzUMVtaf/8JLR6oYopv//cIT//AhCsHFzQ+dIiMl7VNhWumWC/UazzeHM8w4hnDIhkE1SUWpZIQvRT/pjf7u/SgAUPjoih0dGAJBryfYLKZZ7YhEBLMIKjyIhXy3bQBVJepOd1mWtzQEIDmmLiasVUMoeJ/waNm56kNILHTxLz2GKSBUr63/+7Rk7AZkV1BUUwtGoImLirph5bZPpR1VrD0PghIwKvWHntgu57kDH4hR2EEL0f5eT3SpfqwX71LNppT2h3/r6FjJQz/WiaHf/////u5g1Rf/9N3+aqPzUG665UBhz+aaLuRQAAAAIdKo4KVTeS0LdiwClQDGZU3NpyqRQisCaNAPaZTF0VnvMhLzEJ25iUjWmRtpGJUWdibLkZhEZCKKwc4e4hppLTYmi1KJe+Vt5+/+pfXfRNpn8L///6FAIzxB/+xSMawCGiePvP6VZjBtSEKYpf/v+/Y5V9Woe4pkacmiNCRF8gqs2RAyCiDIOb9iyhtf7+6QBEAAAAA8LwYXGTnWgz1i7KyA1tQoA1oiEEmxk4wHTGKM/FTIsw8xZwvwyywssADFpBESnIuswx8BUQgGLwMuiLSEio1L08n7eAQBUctlERuNwlJbd/32caVwhtVHoAj0qmGgiKwKbOiZEP6pJtI8ugRJ/3RPv/////9j1H1b/0++vNU99DGpu8qNzI7eE/JADOCjUHKZhC1R4qkDkBL95FxKuMIQI4OsNBYqlalAlHD0XX4zdcgW+x5m0VgNdV14hAVA2a5fjNG9DS70hHErNpIGgWZpv/G4Bw2CjEvy5YUxQ3LS46D1ZZ/nsTahbpCol2Z7W//KTz+CNj5xkilGCjErQrNsHjRR4qScj2LAZlX1ABAfnFXNq47QGsy9HZAkXkok315MXAA2jlr4GIhD0YSsRl91sih6uEQJxtntn2UJdR2lLwJhyVj/+7Rk7wZkoEhT0zhLcI8rip1lJ+BQOR1TjB06gbkUq3WGGtCmRliwfxnkOMGSUqiSQjuNGjLUQ+IXyRAxe+qO8u3YvQxD///+Vjgf/zq5RbYPgmtBhCXFj6r0AAAAAgLEDzAYOSjKAJTiI0DzmKERJrDEpJoggv5QQ1hxEu8ZKkJBtGlxUONwAAuiIJhxe1pqHUM3f9HyFo0p4OmpJVCeYU57xQyWHwgGUOVB8leXf+VgUgxg0xMkbP//0S6btodN/4v2nxaKu3y73//WNNqaSz3H3Vt3vEPWLXtevo+NOO8XD5c1nUzI1xEVQvLWdCLOk9n42CYHwLyxv/8dzIAAAAAAACoVDGBlSoNtBHgS7JYNSjJCSgdsJ1AHQiYco6YeCw88S1nFAtYBDBxrQ0hlygKQrPUCMmczHAIYoCoE3FmibaZCXNdN2D24iw5e0oXkzvdYOuNi5fl+naWI7CXTTkeRAdGaGlXIy6XLph7WMMvz9qjpfOB9C1DsJ7f///////1jxQWQSi3//L/XNwFBlDlWUcMZRwKmU4hqwUYqB2Sc6+3QwR+etBxZjMGCs0RBngTYrhlNBC1tKQUODjLif5iWwrD1NA33gmFatkH43IzlWZFNXv/eyBQSCUQBUr/4MrxX/vwdEU/ur/+FiGSblUOt4Sl60roaclQNMMk81pGqYaeIZIjoQoLAi/YAID5AEOozpXa5IxUQHQtdVVj602QLtDHopotF3EvE4nVfdmSPISwH6nQ8BwjLG6IE4Er/+7Rk8wZlGE9Syy8+wJ4sCm1lpfAOFR1brD0LwdiwK3WHnmDR6kZT7Q1JufXa5Qxn+exKVLIc1KA9lW4KsoTEfvCYvBUJiyMUIZnEmaS////////0n0ar////6q93MfrRx8x+Ujl9lEAAAABMbp/NwMhUh3TM5FShB06W5w43ZPxggJOjaxV8qVi87iyxRxa4WH2jzTshUQ4wISfaXBNcb/w5nijHFXxGT9rHhhjAbiGi1/wH7yMGf6cOKB4HJQ+//WIGrtzJnrExz4vUcvFdjBeDhV1yYoo0RiBBONAQBMRNNK/+R40Holf4r8ACAAAAAOJiqEOqMiY7HGnwwXBQsX4z5WkGhcpQlJMPetNHM1ADLID2VrAImhA0cbjVwMUI20MxnQQgbS/4JL1McxM2NmjDtDAUc/UKcXghJyDkEunluCo0KVLqPlmcBYXcDPn1iDvAoMGBICH//+3T////rQpymFR//5NUznpJ0liZeruYpa40XZoYDUBAACACa2VuPYQgJjck+ktIS5maCyltRYzPkl24v49j4a3q6/b0J+OTvFkVaalrzuhA8FPPh9y7/tUUjGKlLT/92glsNzkIfWYxiPzaDgjAcMkCX+h1XuROL0PLr41bsIb/5kVTvIE7kHSp6EsWJyQaXUtTsqFxUmCX0w6iRGidkIL5GTjEAXSgHToHgi7L/o2JvsBXe9CA5mO2xoJFH15Om9S6mChBaKqexcAEulwLboDqfaFkuMxnH3CVcEZYbqacr2gIanz/+7Rk7QBkLU3V6w9FkIqsCq1h5bYPtSNb7B06whuwKv2XnqDpSAucBXqFI2VlYDcrTmQ4vd54cP49MMJlCcSTpn7p+1/////6GOynKYX/+qMztbs92Xp+g+WMbjw2PaQAgAAIhJAWkphQDVlNC0RlS5EEbdDshEUFxYYVIZQmBw5WEu+8tPExIEydhYcDLhSKPPIuxsyN00YEkxCzD1nnWr6lAjQIhr5iLHmsZ9s2duozeWr0dh7f/9RqEghCQTDmheUHhHCrkW/Qalz5VUQobj5jmdFmedrO6+NuEkazho6PC+V6njqKTlIpLYbZ+ltdoAAAAAUBt2VGloOg4q4xf80y9PFIFIsIBBDgrCmgiCxoKSwYBPAwzxCLgOfJhIBh4y8AYMZ5YkSBCEKFmCTDKTUiZwptFUrE0waDXbo0RbSy2nS9j1lFBUqOTlQYBnRZJ0J1sbF5E8rOq92EuDAVJapWnfvCdrsgICgfof+QK2//////7M8fHv/82f/z6pTT5pCW80s3tBJZcQbFyoYZyQWoz82UR5h2EIMvWXOBqQ76cD7j5Va2voo6x6hmMyFLJdz1yQkTcFCW+Is58qbvIN46p38BveYv8ZhO1863D//wpRsDvx/mnK15n/ww2EIFNZa+u3/ht5HL32bZJ4xTsPhJUyayCc8IxMz9JFqE1iABgAGAzioY92AjzUhUdjzdR4pZj7tswpdDPyAiUL+ZImNKn1qtNs0CwLQ7N9fEdeBorW3Wkb733doILvUVxkH/+7Rk8IZEjUbTI0dnIJYMCmprJ34PER1XrD0PgdywK/2Ui1A7bz18b7EjtKBtE5APo444fFY4gkopLPU7XSecPutr//+6b//////+kMtf/+xfZdbPT/7dCOGVlYIAAAAKeM5A0BVjcEiUKFhzT8GkeOAnYTtOAzAMDjIntaXI4rZqsBo9lmFLXqfxq62ZYvNuIJMWAUevv3/0MW3SGCGoXUn6sQh/Un8emB5DEBQk//wwoOXXyrL9yZ6GGv/DYQWo9Dnat8X//fPDrvhsmzYUXsebbjtWJJwhDEwLk/6CqYfSogCAAAAAeBqUOBkIsvPIX2kpuApggaFpcNaTOwSAMHYYMAuBQmN00DLAItsa431CpAe3LyhExQFCgOSFjE9Q0SHVL3dLvMGlqdq/H7lDDkIpXn7MYk3UtSmsvkLDOwtWKP1GC7kknpDlO0b6YVKaU//59IABBmKpP4IIv/////+p3qom//61/OiKRV/8K7nbi2zICQga5IcVBoUDGQ4c1hlJkoT1lAJWBhI6LIBRcIWnq+TkTzfNdsFp1QiMqvoGusiW46qRLSyISwxyYu7Tg35miwjxCDvTVrkppM6bzUaAHa48h+X/9NgwI3IXVCBKjWoVNNrZv//7Kj4oBPccj8rf//Tf/7Ef+XC6655CwSgqathJZhcokyBPxR2c2fSawwAFbqxkJpeJZauMQOSDiqVD5IUSQwIMVVGiGIdS04qDWSRG4sHAMRgWDoTgqOpEA4WugKBWKp9NeXvH0WH/+7Rk8oZkN0hU4xlbYJHr6o1rIn5RrRtRrS06AhyuanWnixCn07kosxSqD5OxhmYDKyqCGk8J+Nw/0e4t4vToJsooz9MnO9VsdTRv/aUcgsxnl/y//////+h0Yx5fT+l17CbKepl5PdgigeSVhgIAAAAAWKmKQS3liOKbyaQE7TNc5M4ChjAJpDmVYB+k7UWiqaW4dyOl8YHL6hy5Em5bVGSvsg2/KhwIIpZfkw6/jukhp9S7MH567K7++CITS0jj0Ilf6oOT5Aj4bLZ6KaqTHAnmyVr/+rakHFIlz+a//5j5zx3uKwkg9Vo8RFGFVCYfmq0/jRKR9aBzGI2fXTQQAAAAAQF0X7NKrtPIVDSEriDwFhCYCqiHAHDjFmDwULkLqmFRdNBIw5/19ISSLC6gYA5MBw3HQFOa1xy1vSxYqvWbyJvYJa2jK8u8JuHcniU/G428DrclM3AMNP1KBHBohAqA8VjIiP5jqIR0Z////////9EmHOY/rv6O/zr2QkceiHN0Pg/Go0PH5xbCCICIEAJiVd41lRNSLmsXYOa+emVCE9xgCPpkgXSS5YkuyWsvrP7QAE6Ehe26CSSeXOq2d2XOMD6mymQMEsMUeyL5of6iPKhACKpfWXVkyp+tnSoIAPLbf/2R9HmnrdBXH///96nuWx7f6cJ/l5oGUnk4g6MJp438dLq/0xKgYgB9YUUQWtWJHnOrH8ojKrEuxXS+Z9AMCkiEyFxeuAy+EMPQ6TnGaKZ6ZkkfVE9abhracuL/+7Rk6YRkhUfT4ytOsI8r6q1rB25PhR9X7ETWweiwK32HltDKQlRpuSFng3qseB9STWdtSMLinloqDnUr1MN3h9FBCAcQI30rEh/////////1laj//+9OZqSOkWFSZnKBEDo9HsIEdYIAAAAAJCghFDS1QkS0JGC0pjwvlqPDV3cFCAocDNlyIu8i7aNwjb+ipoGLBXgccxSooksJJmjJmM7VNIcf/+QA85atp0vhznvhf/jQAsH4e/5gyNhKO9BeTDSALQaP+ylSyGGog2KOeTpyhup3IsZ+aaD01lpPc+UkJpZ68UYoRv/6G9HQbSBAAAAAAAoPswJiRCQ4IkSFlkxjyaRYb5OkueXPLxlQMFWpsGWMuwSCAwLMHwcZPYyCYk/EGv+rlq6AQVDVTul8USQL4hJSEbGUAxIeXd7K5F/hFEQw9RdFERS9Q2IDcp2DnEcje5RHkT/41C4+JJL/8///////nIkqgtLt//S7v7VsekdU54tNQfCw0UwxUHBU9AAUJi8oKWEBCLqqxdBxTrKKA4ebxg5bQUCAkA8q6jdLXvliXNLygIoGAsAnJhu0IhGS83a3dp+//0y7mkq+Z42+9QZe/Q8CJgVfxgQiIGxP6HKaLxcQ/+6LVnKZZp5sP+MO/mhir59lxFoMFhE52caCgeUKg0f69GeefanuteGEFOMmbnAAkBoaitKeXmkZcGMIJF1g0ZYujQWecaYWO/cDFzpeIDFqhaiHHogEhs1dQRWNjr7lEfAkEs8iOXD/+7Rk7IZkN0fUaydOsJMMCq9l57YPzSFVrKkaig2wKzWGFtg4EoxN9LIOoiwJIcj0VwZCGU2TpCPHzZQmNGrdszORxAaHgI3/1//////0ZIdiguNf6f6uz02ZTzUN0F0Mggt1Zw8irYSAAAAAICz5kQcCgk0lYkWCAEdwiDgi5URjKBX3JlowcEpkCoRtZalA00XiLcizEwQkmKS684blrcgNmJEXfyXvp3/j8qj4XLtNctlcj5P0X8ilYSwyfqNR3DwUMo9+svFZ0j1v93dScZ7l2lKFS++vv+bWpWkmQEA+8Udwu0065DkRUhYImtiS0QUnLUQxgIgAAAAAKC6HIucYB7oJ/ylAs4OB65pwKIKGGdKBkmqmBiocEp1J4iBkTZy7zChSwDi6S1jKBDs8sBAwIgA/ETYOrc480nxStKauyefptR2A4Ba6t6B1ww2y2IQNL3+5ECckCcNwgKyIvutzBAEov//Mf//////qeURjE//rv2YyxirXtQqj30QhQ3gACERSYEOGKDgcayQGA5MDHAhtVLigBxEQD5MUGDDQcuCooz5rSXjfUKmphAURGtGLEDrTaL7Sk+U3yyYjE2JNXQBSDvtlmLY8MvbAagUirzNn+LMFmOY2Nm6xGiTSL5QM1/YKwmLJV1n/nSkpcFpx8G2JJpZVeNtfrq62n0hlCYaDDaEPhe2FbIjAaRiEkKoX/Womh7UAAAAxh9RY1QzrLIBHJGkGRgWmGkZF+LFR0RSELstbigoiqlWhi0H/+7Rk7IZEdUhUa01OoIxLSq9nCm5StR9NbbU6ghmwKz2XnjBUXKcHIQgBbEmDnAyHIgBqjdIa2nY8L1JETSvE5OhKo1yZKrtlVS8TyGp4TKmGLcaeOlBIW2VXQKetM8aC4SQ2Jn/+n//////Q+c5pzf+/ZH5jMk9XNR29JgvK/OKrOQAAAAAKXUFhJbhaiegVCrDnOFJEIhInlryohZAG6dALIS7ZBG6bVI0JnaixfHGblrOm8UTf4OQTHdWrZ/dWDpgqOTph2Xfyf//0RI05/h/eO0km7qHP/7iDRMSc7v/ntPtzW29RdstrrR21atQ6M0QNTNp1kFY3tqHPUJRZGPZ79B6S0rCgAAAAAAAID6d6KTloGMgUxUzEflJyNRh+m1VVHVgpbWQiLX28Y7JH5hiXs5DPN0RIRtjCa7CVqIywwQwxM6SudRqAhSqV1VjxCweByEk9sfnBu2iHhkQgbY37lc+byNBSkF/////////qhGu3/+fzfVqIgj+JiH7DR9zECRfHBFHFWgYJuxICpicKpUNLnQpnCHVA4xCw0TZL0+VlNOZpnsLInXRosyqV6RThalsjxt/4T5KBZldJ+2O/+gPgoP+KTo84pHyX46PFyZZi/1RBHOHjOOGlqkc53Xq03jArKjhqGuo4cXYcHCoDXUlb/+UkEOlLYGCA8qqlS9S81V4mpQBI0AqKrUigpcYWHYeEDmEIuQvSveTtNfqHkwAIND6zAuSkK2Jdy+YUspOmq7GMtr8hIqSGLPP/+7Rk3wZkJ0dU41ha8HtMCt9hhbYPLT1ZrLztgdUUazWXpsixToQ/LCGjZMFwSVRjS6ThUSioTWxF/Zv16IlxF6jP//22OCoRDX8N73kwHLcFXws1VADAAAJhUhAKNtVUDQxQ4u8aKkGGGxqYl0SwTNYDM05CwUYGKjZm06H9K2g4kIzAYpfB1C7ytj3P9jfEAlk7E0s+/9eJtYQhEhymln4KkX/+gBIKANf6ob4YHFyVHX/YbmA2mypCf/KhQxrDJtvoiMPTOos+VBFqOUamtKnC5dtlVUjWPG1ZpMTZHIJ08z+IopsMyMAAAAAADg9Q8IMS0R5aAokWqOuAt8oEVQUJiMwsUVVDfGExxYF6muuA0guIrQvoBziRJvFrTMRMOfWojLKQSC36rE+OrhD15FlwHYSBYbasKCLU1DwPE8kYYiTPltRJxumU0IB5qB45MzPd56+NUPi9/1RK+qLQv///69UM6stP/996G9FIKzLat3AwimiMcOKIYgAAkKuOLJ2Rlkkk0OaJwXkg6IQiWNLUYiMkDIL0R3tcFI5Z6/67jspBoiExaIInI6QJjEHrDgyPSK7XJu3UoqFrYQWHLAspEG/lgSMZsk/RIsopk4TpFf7R9XHag9b/4qFGpGhy4HYkpJsfr961RtXcb7IPCgudbZXR6VHbdxvYr/lral1klgd/FmvU+zst+085oQwVDmmcreGDgxkqMFaaSSZoMTW4uB3Fh2yJFj3bBAKWpoFxFXsiQZc4HCCQhYAMJor/+7Rk9YJkmUfT00tOoJGMCp1l5bYQ4RlRrUl4ghswKqmXltgayhFD2JscxAk/PiYxhZFenD/VRwnW0asn4jMplO8MlucZI7N5f+oeOIKUn6sjftr/////3////6HOchijqq7GONiIbRWQoorYhAAAAAAEThAgSrprCSJkAkERZM3IaSXcKBhetN4RDDcHQ4Okepc30GxyDWcoSEGEk5ZNK+eyA77dGumKHrlbi2sA0dBL2sKlF0AyiwHumn+cGWPAentKWHAPt//wJTgSImf/hVjVhmMD4+FEV/+adZnFB6w7gNEhMUjGiptn3IcDA+LGDZ///mBhkavTGcRGo1wIAAQAAAPG8CqFpDnRDhi7ZFu1oFNCgD0omNGTXFSxG4j8jCWfbC+z7y1AdH0lTFEjZdElMHBFnRlrKVaR7XJfcdN+ai33BoRrF5yjl41PQ9bOCxFEPpJCUEDE4GwUF4ijoZF9p3UHo3BaDwib+rIW+f/////+aTYkNG9F3bZ0zGSlDXU2itUnNMzRo2s0T2gIAA9DcaaSJVuZAIA1ATCxZIks3Nh023gAVEsy97O2CzNDHWiNjCDw4K7LWisxd9oUSSkKpF5mb7ym/qFNa2xoAAOY/ETgD+fuwkhNCwSfxkMS/9B+cNhadX9GYofONuQn2ICbbvu4q954syCd0pFSGaj2YgZiLe6xZXlJUgIAAAAgPwIIBwEy+ZS5pjQNRRN11Uj2+YCFDMKEDEyFfNmikwmq0hDi2VQp701pAnxArzP/+7Rk6gYkilLUa01GEJCsCs9lh8IPlR9TrKjawd0uq72GHtCNB7M2qkkkFMdBEaK4tVUk7LB26dNZ6GcK3Tn6jI6NwDB4shQt+UUurW/q3//////99f+vvOa17OyX+queyLKNSEaIiAAAAAAEKiAMDMNLQ5hQpV5gFnvsl+HHL9Y0s8L0DCnEINQyp2MM6spMYzCM+oeRR5sqlaf6dzFwFMAgabBJEbHXMIzFG5DjBojyxhU2Pf8wWaPgDBG//7Ate//4OZMND6J7/9zWbazg2PToredn4lG5iETT4JJGNCSbWUGObn7UOJyRGHDbqvd+ez4CN12zdb1IFAAAAALCrOiJmywRA3KZrLg0WneIwMQQUT8EYclPDBgHR2MpDpqKeeMrArMWeZ4oRAnnaSjaMkUIXxTmEQpixe2AdiEoeiFtMKAC4KIebCu2UkakgK9MPIswm6vN5aypGEnp/RVFqFF//6UBEGQ/9f3/////+8hnT7dOmzfaj0X7dAzlaqIDCaoMJh5AozAV2BYlPpXbingmBgF0MPgFl4JHVlIo7Mnle96jLP2wlvX4cuDWCO087vsEVtmLKsFFObsS96F5pgMNsR6WWP/C7njcCpb+QImlC/4lj4tEpSg7+eVVhe5YBIWG0OHnTfERz60nIqyCBCKHQqZLGQ0jjG9//4HFa+qPdKkAggHxFMAkX8jZLWSQcLsRSReZKrhbgkQKcQgZWFAskSHgdx00IdR/IStGZkm4YhmGdahDUg30qmW8grb/+7Rk7QZklEzUazha8olsCq1p4rYQGTFXrJ0aggMwKz2HnpiUDosSnOVXA/lUdztMmHsldHtNK5JHAlbZcoA9Bw1pv3FY8IgPVJnfsY///////6uecv+xrrnO2tpae1fx89lRb/KD9Z0AAAAAAAQ8IhgGCAkWnGk0AQz2nFOJSxtSpSCOZuACRBpmHwyy1s+OmR0pEFDN9l0Zrwk0IRPHXNfhmPKCsKbNBcZhp9l9ooOdewXlO/8PYQ4rHo///5vLyYz/8knB+PmX//sQScfX7azUnr/UnlrjjdqQ+qplyqybGzw02YkRDDr45n2HV49OYJz16aHEAEAAAAACgfEZTSEs4IXO1HIHP7U8GKMiZe1wIEKKUNDAmMwJI11DtAD6u7EASwvSoQsdgaUSkVDCYpMOVxiIpaPSypZjqOiULGZVoiJTR/kyGcNE+UN0hKiZ2tvsPCWBoOghzw/TLjQZPCU9P5Qe/Vv////+i0PdV92oTM9Daz3lpXO/Z6Vb8oiQAECavGRQYFFRYGDNVL7F8R8QjwQgIm4ThBUwzhAmpbA1HKN/VflGmEv1YsqHOY8LeJ+poPnTSSfe2hmYjKZh1IxUqU1v/QgKB+GYPCn/MkhMS/j5woBoT/9zkYmYYj6QHMreUTUTq56iCssJciheqUdT2UUSiw8pPN+79lJ3z/1P+TWuY/AAkB8hhBgjuILPoyciJNhhuqJaeKgKtopChMLWiNAv0YYsNqDrHTOhqLmESjAl0oMFkAuhfA2SKAr/+7Rk7AZkak1U61ha8oqsCr9h58IQwUlX7Sk6ygwqKvWXlqAmOqzdJgiGMfhwNAw0Q7cVOf5qnaesRQLJrKc0USapzMrQjY7wPDVjUGTM/+R4fDoOGM39W//////+vdL/6N7XerWjQO2yiS4qcIAAAAAKRARQPVUBwBaaNSUQT7RpSBS2j0bAw8v4Y8GCg6gTOUNITWYSrIw9Qx3I4rC2dSEsSUGAK4qm6zoztDL16vwSAFh3/Xay6BstWHCoiAHBIAgRCz+OEGgSRv7hkcLmT/SUKuWlCpUSyppIv9G9cHbXMWLZpiCy4IlHCDEaKQnt/mZnxEz57ULSgAAAAAAAVD7TRIFB8lMSuQ4t0MPUt4rCW3nkNyYkCJGsEX8SvS+AU6gzaJ0NKcxZiz2giRYAUGSexDC3CaCtO0mEifRwtiEq87VYgku2KQmrCX8vpBzlTkdGoeyD9f4UCshU15Xk1af5YiPA8DNv+Y3//////vo3/offdGsbtucSrzy+UsAIYwLEF1AUAiKhzBBBJ8+zJBGW/UpbMmgBCAhYDR9MBs7NE3YFvvsFwJEeR/lsqSLQIoqV11oAQcUefUwp7t1nMQVELCh4GqaW2tfE6J4KAiDoBCEOwcV/mDqQOo1//4bD8N6+h/vrPJ/SR15xRG+a+Z+MV9zURtg2jQpoWqYNsTnS9tDlMvckfmHp7AAQCyYQCMTnUcgRAE1AlsQpV4HAuWrtMPADkA66jKNEpE1nFYGqkXrGRIliiUzkflil8iD/+7Rk6YZkXUzUY0c2soYqur9l56gRiR1RjS06wg8wKrWcHfAzIAE2Bn1SoSFrv0v1v7rMq7JIIq2IJWQ27WG9Xw5bpP03VTexKrYwPBADgaCScp7XxaRC4PRgRX/zD///////d3o//3+y9+m26e09f5heuIAAAAEh+B0k3IQgS2bOn0d9aj00RPKUIdDDggYmNsSBQDCa0MQxSiKhBAwTqdm4I6Eac0CgCIJZAXSp/wulKNEvBUtr9nykYnLs3nWnmCC26/8SCw5wfiv/ggwPps3G/8y1z8EOVL98V+vxQxVkeoyCnkcUYzmWIUHObiPJH3/Bi0wlqy9vqBIAAAABAfipiCytqj9spmDBtAxApS1MVNsQNXiRoaeJFSnhD7K2sig5DYANXKwtOVTsMQn0yuGHmf1SI48jgWEYqEimnFUZYDcVRAELVSYQRDmZV7eRdzFRQwsFliS5uXJFRKc50b+v//////11POmt9F1SlPtXVFZXVUuOhOvfHnUASCABIdKoVAy0XwVvFQqURyqAsKBIJ23qlocYBixtEdlmCLj/KShhnAKgCYLsRo+S4J+gggQQA7JrIpluSJd9HCOk0JSf3UHg63Bew41S2Tf/QBjqcf+GOHQQOAiU6Fiz+dDlH0ZPw8QxAWVThAJi4uMILx4qEDh5hjC4Mtf05hG3XosUtMAjKJ40RSFmpFDxU+GDmvQUKocnwvHIt2OnHskLUiEdEVBGGLUkMtjQ2aEvxNIsHgmfnwCFQZ5WazSdkGz/+7Rk5oRkNUxU009DcILsCs1h57QQrTlTrTyvgfmuK32EF4GJ5Lj+ujPQHK6CSzrhLji0qobMxNOnOV7c7FOCBsFMQ3+pSAwfD0KP+Yz//////7p0IVv82S36/y6IvR2Dh+tD6oYDQAAAACg8OBTBBWRLboVgFTmtkpVpKGpCFUGjklCAFhMJTDW2sA0Jikvh161bkO7+MhbisqZi7tIJn7h/tl2LErpYacgQAGoAthaicKP5BSKjhKJ7/s0lX/8HjQvYemV/8RwZK3wRQ6MZ9fdSNMHodc9MJjL2g0QD8a6ZMju4//SfJJOKiwtWu1WYAoAAAABAnhJhgQWpw/zJmJm1SBkGTg5AGnEwCpRDaEQDWoZYzNXhfqH3XccHAmCOGHhgCC4OBJlwgxbSd1BABYR4o0ly7H4LYfJLjzKkyjmXRB3MXMZzSqWGIqWFGsiiS7OrlIgJYT7FZf/4iOC0akKP///////93pYixvtj5eh0jNbc127Hvkh1SB1UOJA4bLJJeQkWp2AAIxCAtXxYq0zI2BwzhMlpVIBUoyECaBSpp6uUBYlblOj+E6ApsOTOQxbeicmgtSJ1R1XbihExCiTGumZp9/+K2D28/2/1GXYS/7XViT1aXahK+a7FlFyCplKKjOXUusH5VDChqhJHzPDvF9Ne7CBAecseTQeLgOmqooud5yl5ZtbqykSx18wZSQhNI0AALJxJ8y1akm8Ach1FY2OQX5fUmzhyty5H+ujbcIJMzHLAXQuzNdka2U7/+7Rk7YZkV05U61FGEJQLqq1l57ZOOR1ZrLzvQeCuazWXlfhLvydrprYDkUR/pWyg2pB+Z+fA3//CRxsv////////Jjaf//d/V/JQuZH+NgO2lwiAAAAAJEqE4wAVLQOFFrEP0rQplYcWBY8WTRIiRg04UBA6YtZXS/V0xqGsqympZRCqTMAhpFST5DAJaUB2EBTku43eEQ+xNMlQdBKxeTtM//8RQyJHwef8x/AfOIgon+Mes2YKvILFRV6h6r2rGGDzRtKsGCIYZZL2fpJoq4RB/goJJrj9P/tobHOR0bsAAAAAAHBcYIg4IvR7W4gEfDYDAhABhhc91l6jzAltiEG2FmJfJMJO+IL7eRCYDCoYAWIzwgJL2L5QCXFmUY0yB8YE6ZRwjrEuN0ScB9k1hk/OkIaok6D4G8LahC7TkHclUKcGFVq/Urtv9PrzBY84P/WT6olv////53QQ7//8tCo1Z4kVFLJc9ggOImw/EZUAACBJ8ADxYRlG6NbAgkRDTO4HPeFIBcirERBAFFmLFJBGHEpsflELBAFglI7cErEqUrV0wG4YO5V02GpFnmLzpbMyT+iUTw3b84B8l9Bj5nlOVEOLxVIRxu5dXJzzuP1QnPYeMn77BzUbqb24JbiJfmpXSTAItNLMQ5zQZQ4xXKgEaH6ROFmZehnKfCmhXLT9iqRimKSZWHEacDHy+jHizJduAqRJOHiQYl2BiKuAwMAhSyFzFgAFihcR86Gqiol1kkJBUUhr9wWzqPk0S2H/+7Rk9wJkb1HUa0dGkJAsCp1p5bYQFSFTjSk6wjmwKrWnntjMXR6RZ1GEriUk9eppvTxoG65eDqTeYdMDJ5UCg1V/1c/6bf////71H9H/p/Po5qKlVVp7sRJq5Y4cDyy7nZTZAAAAAAAIPq1B14cLEIpdwMGMKN5FfVNdf7JlBBUKQNUDGhypTafuc2vOmW+ljcaQ8aw/GRllWKMlmp/L2wyePNbZxAT908633H/tfBRf0DwDNif22uVNRhLf/dRgzjdMIC5qKj4rxuv6/j12nx+WKUUEmraQxW2a0EwkvrgavoyooP93/Am7AIAAAACwnQYKBSoSx5LcwxF4AewIFQVlSSAcHFXZD0y/o6GBA2tEoEDLQhxH4LlEzrHnlL/grj9E66QfNTeGrPA50odMRtZjWQ5nZDsIQHQbyiXKufoefp6NJcXg3FgAwiNHx0hebLKODpEbf0f9P/////0cgfc7+j/dln7km1VrV0VokBl/TVXpQMwAQBQ7kKEBljJxxRWX9MECZkbMsUAi9SfCOi0xGbC58WFjUBeXFz7wzoJcRQ9pRob3QwHc0SXnv2uPeZQF7QppfP86m9Q4UFq872MYa9aX/+8bJOJJIO/+WulI9LFulLSWdt5WuJzi7vppETKa2JtLlmsSNWixMaz59HiV8iD5Ez3ykAEBcqiJipAjILP1ztCPm0ClojtSBQ7Bhg4CsHaEZIIO3McBvC8s0nKp2tdBZJ9gwgEKi7KIcLYoKJ1RixRCwtxzo1CyMRj/+7Rk7oJkN0dU60VOkInrir1l56ZQlSFZ7T1tgi4t6rWXltnTQyK2HUX5KD2IOYkceL9pLiXFXsdFcaZPiwsmoLuH84+ChrCgDqn9jv//////5HYVPM3/+k330UQKhiCxyPQYKMfWD5AAAAAABGCgkRCEnUgW6kAFyT1JVYFWKVpzI1GYQmZakQtdqrIYft1ORKbAwRqTgSOEqPMkjyOhgQ7KWv0VJLMJmcsw0hmpppurgudnKbP/QQ+8T9z12ms4C7BEROv/+Q4OiZFg//9i65UmGoYiUv/Fu3WjkSYccxhAuZLdy2IOasQDWEO1mVRZKkAAAAbxMXliumuKgTROtIDg1MWdL6gp6YPYBKQOtp9hl4xWQ6wDbJNizaZI0CsYe7EjASiagoWXTyS3OkwGitXjaZFRW5nCbqc8PuEtmV9ZS5pfRaSmbSE2m+i7zuFLEkHkcllj7Qt5YxcvV6GGr2Eou3yQVB4JEWO357P//////6kz0NNc3//m7fr92/HrKNkCEjei6mKoaGDFjiMMsQfFJ7r5U6RVZwkMCQpMHlrQIzEx6Y1sl6QYj7aUVJGKIUgX0NncYe1OnmaG0GkchwP11Lv/BwhufTMSMH2Pv/+bxKcKg2Dy4I//0brnlIIT5r/meRtcvQ9lV9Lt3iB4kBaUDQQhtR//8j6VOsZ7EekALi+FiQbloSn4TrZ4YubrCQi/0CCgbRyWZOsQihjd5SDKnRU0gSHWwIbOohwSMVFGm3JQ2WSG/E472mhyHqX/+7Rk7AZkUEfU40g3IJALinZrJ34PvTlZrT0PQgkuKzWVi4iZW1DkVwpY41x+n/bhLq0li8xO3pBF0DhMAQjkoTqPqnKECxE/f/8O/8/////9XYXcIKp/SC2NLRmNvXkfrnHJ2Amq4EAAAAAi9R0SKEyVKHKQ8YgJiKpSQAcaEMtMBD0KSJPLWkwg8d6/2BbD5O8zdrkVL2QJblpENjRRMwpBgTA42rmychgg9iSi8Pg/vj3jx2UkxGli36R4eB+Gv/9VfKyUioZQmd//Urhbk8x0n0/Y//0XOLju5IRXk6E7rOWjwYKG47SILSKWV1//w2vQt9WjUMl3/63F6yAAAAAADhO6I8evKbQtPdFEylAFDlEVVRIwlEDhBj2QYlM0bEAndUi+yK9RuacrzC5F2l6FZ2XAUIV0la/06u5QmXwZIX7ir0L4xgeniLtPCmw2CRQZi+s4kqyOx3hgPABwACSKKge/cPGDxIq//9laxmv///+tR4wiPE2b/p6X1MOMX+WpeYYQZ9DUJzwIFmdVQRCQYEAxAvGTBGsHJFl9mqvojW5wgJqDFBqIRkwImerhCyNaFUSVOF/mZDqFlExvSEi1gwbM6ZIMEPRMJRKpAyfIpPkuKWHf+R3PX+HVz5wmEsmL6P836ler5obqKT/bP+GVZcWXpG5qeYxdaIiZdEk8WuWKnPO1bjH0agAgBdfZaxFdX70wG5BUlWAQloZRWQkixK0PQKUoUlu1U7MhiD+l6kTVMWwpzBUhEC6j7Fb/+7Rk7IZkslhUU29doo2sCq1rB24QCRtXrT1vQeSwKzWXiqCm1QoTQFuwpWBXOZVHm+Wm1tSxwwjaUqVmb0PYjuiK1jy8LrIt3+X2v/2ABA4V1/////////Z///p+ze2j7NUMJIvMgip5jAAAAAAITIdnKVIAmIwDcVux0GxiyBE0L+r2LfOaaNIRGo2vNn9FvcZL4slZSwAvE+imLXH8fZI5ljibympv5mHqURA0wHKY/OxGVPtjJBFAXkDp8qUKkA0nExP5xxKJpUk8r0zB5UpGRpLR/y50kctylihxt17OBYpe9ODcDgUisz+hD2Bz/akKAAAAAAAAcXt1Y6Qti1ZfdcSi5k9DoZcYKBEx78glJjJGAXtMg4sosRPaMtNfd2CwIDmQUQoeZppZlQ+Vq8TDbu/cB9EeS8ek8FImRNTdfXljqUf4pJdw5wT5XqVOH4aMy7yXwZKfJtA67bon/43GoEChYv//1qh23////uaoSiggPjQn//ZFezmHveiqg8d3QgFxazJZkGmrGUioKoSV6VRECswvQ6xpxqNLDT6YJf1vEXkkX9uU+9dMMpVEdRCTIQ4eyGMQZ4z2fe7RvlQNg50Yzs6uW1ZH1242Dxwz/k7LUebv/ofAwOOn/VrziR80nk/KB997lo65h1IdHaPZ4dzEbOyuqxGbhcdZuTZPu/5mZhAAH1UaAoVHtuw4J+D48tAt150ykUlpJDpAFkBJRchWKBFLhYcWdMGFUrEIlFWXB+Bvj5FGiEKZFOP/+7Rk64ZkS0hU60pOsJmMCp9l57YPHR9brL1tgfEwKzWHlqCE4nqVYVou6bQbrLgepeUNQxlYibFLO4saORTmxR1Md7K6+MX//Zgrp/Rv//////1ul////mOpmqRDaZh6RjW0EVECAAAAACQ+woWOgKGCRS7xho0nKYVEMrTaHglLlGZpAoXKRfBoThSvWlHEW0j5WxqExpiCX6goJOm8jxTUdLZ/kra84KYhmNA7DGoO9Gnuv/8ddJR6EwuM8//fXMkm//3PefInedXvu/0TaA+r/iN7Un+pxTz51p6a9dQlDlo0FPsmTjNyDTSsyREib/5SoH/h/gAAAAAskStVntI+JotcPu2aiHBQchGnJQVHRZiVYGmGFIAQaMbYYnwwdBRTAuaecB6wIgDKR3O9i34985DNS3DoVzF4i8cXYLAygyII81y1qs7bnDJfFGlkTJwClWxsjInAVwwyXxog4sCEJREi4UmeWFY+SYoPN+jf//////U+aYq///95Y5DTTEH2lXKGuao8QDmnxBgswWRoQ7hEAUqUuckRR0rhIMldKLIVBioYeAreibp0evl0DRFkDjxmxADcYPYejXIHIo+//2Jp118PLE7TjS2D5j+NSoxCYNv1Y757PAYUTTWz7/n7a2lr9kd4xI3Nro7e72NqWOUdp6ocr55QqmPssH2a+QGwrWAAQDneLvN3bs/TMUrT6VL9vCo6RArVARgFnXwQzbQhVJV7TxfV3JoxHKHthf1DIvmmqLRABn/cdrP/+7Rk7YZklEjT63hLcJVLindrB3wPHRtXrSjaQgqwKrWcHbgAqLS6UvK5bKkO7iQ1XbFaaiMnZLNskuS2WR5VdikxIbY+NwGANF5aPF/ug+XIFzW/t//////+t6J/+n+02k5tU954w5xvMQfqlYYAAAAARJzd0ByNzyLzQmIhmblNaVmYaxNiQWFEoIOOtbai/knwm6ePs3VJPWayRbNXzTbIhjLpTPf8Y49U1L1EnAdiI3Y40yV80EMD4iBYJPyMnuPHz0IzxaDwQzDYnd6G6G6PW5MxIfmVdnfWMquDDBaWECTpFTmklpJpQp/dOwxlaOi0gEAAAAAgKs/EIFSkeCPC0KVnZFAImChZWCBIACBUDhCvDARAHMuAR0UQV5Aqq0No9o4BUCgspECjgYFBAN/wAVTKnkaLaUBtHcoCfqc5ywrOoyNcxT0enBdicnEiTpFlKYuMqgiPCjOsv9fmFF//lBqLgJOY3///////6Lq5q/7dd2e3blW/rmjhJS3ItmAJGOOiQAuIDh8cVY3I5j9YYeEg4WkuBialQKCkRBlKGbOpzW0EgcDL2ERFDajp20gRezwmBHK9xjfZp/NzPTw+hETgeuk/N/81Gzsn9//+dJLzAl/tveSALDw6iQ6+HbknHHLfCUnFl1r3ar3xDT54/wobEpVQ7aTTY0mWwigJjAxKja/UxKEKRLAAgJ3hKH1MhpR/lMIbP5BaghIZWRBIWiFEZFGlkgB6gMOxVprcAMGuycqFTkn4eESREVP/+7Rk6YZkMEdU60o2sI7r6p1p57ZROSFTTT12gjawKvWcKbgR8zIQvXA1DDSDK+ozKH0zaQ9EaltyWwYs5G1rzMIelKlcHP49FygnRDDYRhBEjoaUG3zhVAjLs7f//////6fshOTFr/R+tziI7msS1rPdnMPlDXd6tqLZhSqMgAAAAAJYoCBwlJYIRswTraSd90g8tNHBR1dAXJgY6iSuGJD9aNth1DXKgNNvc4B1C3p1QlY/UebMa42u3I6Rvg5w+S8tzpVf/lgYDcTif/8o6yWrxieIBYBTd//5qJr8YzG+R/xJ1J1NXBR5li3Ucq3RgcjQUFChr/7deqBAAAAADAfFR1WPwREwsv7Dh3slYbLUJS3l3JKkRy90bkLhhKVPs4T8GCXdRmMXwhwXxwkxLmK1ClPAUQvZoheFWSIRIm0jj0IZU2nmI6HJeSsROGXWDDs2r9M3npn415gUgAxUKt////////zCU5j///+dLtZUZ3Q0zWbIT/IiN24AABY2wCKKdDwIt+hq14/y8mIrKfdWkiqFomgKvmfv1GcM8mFrlYGp1X7KMl+LfuBU0PttvCq3mLd6zL09y+Y1eTtzkN3P+XmLwGQBI//bTnO/hbyIRRyYLX/+h9ur49z9lf91G9h004g1H9HN6bU0zKj6ZJBGHgaSIZp3P//Jv6iL1l2FZGAAAYKFl+58twxEvMnOf3EhCByzoOgDwi2BpkKNpqFmUB4QmlYvwQIO4WAG5roSOFg1XikMfQmwIt5OFrz/+7Rk4QZj40dU409D0IGsCs1l6n4QyUNRrWFryjCwKjWTi8CqhcBWxujtvI9qZ4sOsJSQVcUOZu47SaZOtQ9fy8YWrtWpj76Sl/9KF0VBM0NvvzfPnEACTiDf///////6VCGN//8/dJWXXovXAFH6OIB1koIIAAAASLjEDAk1wIXBcUia7gPjJ9oQpGQygEXmXtUCU7TSk+P6fJfqFSguvtphMUZNH19sjjlveUO12Vz75L9ZwoHJHRfulo/x2MEhC1Dtb//UzSSHqP5TJY0+59DK56ndGUqb/r9OMNicdU/oXSmh/r3kf4uWBgYBmDFs5yGZVCjgwEAAAAAAHF2whAKiLCw8MAvsbOYcBdTqCAW4zIJARrBBja9w7Je1/kEr7LDmlq7Cgwsk2cQXU0L4QCv9Urbu8OAUxfymnICZCy2BV6xGBI+pQ1r8VWQpBC1tmULVhgWOkQdMDSxrEhe82yBCNQeERXv1P/9N////3+bNHCaN0/m6G8x57Tv/5ZB7nC1C89HAIALLr9BAwcsudNYtHCQnQIQVQabDDBR5IHCq6iymsj/7kFPW7yZ1yn7LWau+2rsPs4eeHMpvORulDLMWRUO5RBGX4RoBIHQIv/M/o0wfCxdiPzVMuIx7JWSqur9vCpx9qvXXjWdvPKXVtJuwegBhZiv1+r+2mUBFAHiGAotRVUjtlnYJBmEShUaVCa7UgUELiZm66CzkL/eq8nk3SStcWa+jtonJ3vgjbCVQrqmm8Ufl7xOLCI5DMLb/+7Rk5oJkFkdU601OoI6sCq9nB24O7R1XrJzagfawKz2GF0ii51DK5twIdKNArdkS0GAW0aTwrTbezXJlveGBwo8Exj8iv//////+6TXT///6UEmf/4BCojnOPFiqlAAAAACIQ0UBWMpoJrDwSi0cSlo0p3tjLhNOMlFwAAsrhhAYlRLN8QDA4VOiwvxTCcZ2tF3xRBbM0CiTEFwUm4602+z1TUBCA3IAvtdh69v85RfttyX9r//xEJAJP/6qXJOJYgyU9Nn/arFzzpUVJElx1uf+O1m7FUDU/Vk5IDBLozOnSUQiLXOI9HBvhZAfyKHrLe1+iCBAAAAAhWHQi4TQ0zlg0ymCCDswxVeNgIi0/w6gGoEQJhtj1Y82i0hG0IalX6WChZweJQ0fRVJYy60+AKQUCMrVq6gwEkboqS3jrDkXLAfiuqJ8MaAvo52aynRKfLwdbPRZSY7EbbEmfTW5ijoOj60fnX/dL////8+vZS7KNU9ttX0N2pOnY2x95TPaAmNHQTliVX8BSBAAAbiuFdsTBiXrUFBhq5ws2itj0qgUCLUsmHWXU0WHWeiWwrTFdSykzTmNDhSrAsrbyLP8PT+L2wuF9///LPF//zgUCo//5a6FBAPMJsyv+lH7jyZFxgglJLR9DXiSrlb0MfYSsOooXGygwUssJAuWOAB/EAw9Mh+ZqiEAAYE7PB7YqZ9GcoRycwssLuZqxNkqGSLyFjQUBTGHTUGhqDZx/niclYzE4gjQ15ylB5O68MXq0/j/+7Rk8QBkrUdSy3hbcJSL6p1l57ZPtR1brD0Ngd0vq72En0jftbrMwcKrlYu0zlMLHiMbOFCzJxqrGRQYXrK9/4ekJy40P/o3//////7uOnHK3//PPfZdVn+dzVPU30ILfQIAAAAACDooSEECQ4jWWER1ZyceKN601JVC8oVJCyQkEsDNy7uP08Ft2T7R8YtPqwurDKky61Kl4zlqkucOkhuJP5QOCmqlfS91/+B5IAxPjoUOf5jug4PBkRKN880vUlTlhROHk1Ptc1qrbQfN9hDomPp5VRBx+EtsoEJEUG3DEIlg49rFgYvXlLyAAAAAADSsOAFEwYAOgyxGlvDetEAYZRXSoRuYoNThgqYi4gsCickeztdTpLDmCVBTNWFoNwNAaMwWAL5PtDa9F7uU3N83QkcscWHX4u6ZmwNVaadufdbbeLHikLjWDZYqBQoRSXj5KZiaBAMNIWP//+ln8rqnf////3ZGRmH6f/JPmYJO92RnVtJHerlUeX4AETvgkyQAl+rwVripiICcIQGbRQ0u0gSTsdXF4Fub79hijKVnSqMcVWweWGkl3/RBhtmsNxyNuxMMJeZp7XWvOjGJJAn9QqDgJm/Of898wIwpmm+7I8v+Fq0i4neoMc+oJqvS2aZkscKsYetCCH4uA0Iw65LUdI6U4N/yD9klDQ7YaI43UXYa5FKfCjxQ1jBiLZgE1PpDp5org4WGlbWVnuInOz9/UUVbRgwvahorIJBmWEvV/1LSISSqN0qXyIKPC9D/+7Rk74ZkWEfU6yc2oJBL6q1lIuJSSX1VTR0aijwwKvWTm6CJIuulDM2HGl0llDz0LqzbzNUX8yuEyiletr7rMtqvw/r/vSoDBLT4el5ELhACBh5URWz2qNBYJISjpH+jf5//////Y8gcXct7/T7PtojeuneST86Y6k6hkJZAkRA6WWBQAQAAAAk/1D06AagJCF3BGG1gLRg7VE6B4m7yezjDgW1zszJcfK426eJAhFg5FhRWLl1mrNKXy+EQM6OKoWZ6CqNhE//9XxgIMboPG+yNsrUzTJzmdXOR44UZTScYELEbGUQ04oTlRkEsqDcPCdkVqsrZz1JxWktK9GVq/wYAAAAAAM5fUyQS5qCNwgQDVOoEaJDi1G0TkVUtwcC68hXy46ma4mzp7v++s+zRwmVwEIgn6edKmQNBUWnBCVOezkfqFD/PJfXdlKp0W2vkSyKdPNUd5CbiAgMBQXMKr15RBZV/////////U0jNVW/+/RN+c+v9lUqTFCRcpGBIyAAAIFZwYAApuOatlmSsppcAkGHApQAAABRnL+PsPlLLiIz3Y6ur2BoyghjDf3KhlbTkrWuJ1IrrCSHmH4OI5rAUAIyZNZJtjTBVHWXa/casCMCmq5sv/////GwfhMGQ/EoOn/+5fWHUjoLrFroOjnisq7hRIaaOVA8AC5PvUNdtjDxGLDYynqr3GW34MGF2sKCACFRpVCBQzQSkEJIFjMrLMLuhsCAS7yUBnRNpylNF8o3Urbq/DgAsDSQBxIP/+7Rk3wJj8E/XeyxTYIDsCt1l6rQReRtNTeENwjEv6rWmF4AKJBrnwZAzF11tkoNMBy38mIk3NiK8WGTDzvEu2An7h9fD3odoYUxhxFFtYZTC87IjzzLT/z8/D4FAgYOHq3VX/67f///6djEExn3/s9XLkWSv/9RSIvmDCWpwYSMAAAAuz9nRFYDbJRKwjhtGYoYhZMfmV8EyEs0aJpdt//3M24q+35/dppRF4Zoo36DUsIB8RQDiCEyp/HVKkRf//98bhE6p80+zJt/UUF0OdP+stqXv1v2nKubOb8RuyoLoUdgyaJiANJKQPQoRvObN8CAAAAAGA/gHFFiNXcgWFLR/Cmyd7lK0PCXqQCr+n13MgoqagW6+rd0IVevQyEuaW8n0FptaLSqaML9wjrjYTEldtxIBmKSanmDi+A6UGhQGAcn1otkRmXyan8K1JUIxIGxcq3HEf//////98dNMIP/9//WrHv/1gTQef4xZQgkgAAABaBblpBg4u3qQ75nZSIqpkoQJbooGWLIHtdSoUsbhzulMU4V0IwtAbhxjMFRBuIyGGgk9FHU59BG4OuOSnEuiM9hqgo/wXORAiDh/itQfN8xXlBuJZciz+6uxsD0khBdo4/xvHLpT9KQHYuOPkoaPZUYT8AKOWEIrTSUqJDl9/2XCIAIFnqfBrDEVgEhVLz7nLdtwKoDtsmA1ahAFBC65QGNJIClGE+Q6ZbyPC1lLS7C+kw3BYYDRQYEgPZWaKhHcXpciFE7LGTcJAGT/+7Rk4YAjnEdYewdNwH5Lqt1hJ9JQvR1RjR0agjyv6mmXltgokLUN9hFXuY0JDZGMwtHG/fK5uH2g3kKFB+7YnQGQOiN1+n9f////yfZldB5OvVan7l7xrMJHEtlq87HAgfD9hMFFmXAAAAAAANR3QJlUCl6mSqbBQGGsMEAQjOpkVRmUxgey5h5b1luH6QacAeGyt8m436odewpsCrypjCoXDuSiWdxX2lMZzggsQkFFrL/ceMEgIO//4hAcNu//pKNdk4TyQc3v/+VnyE7XSQLzp3/qGXUW54f7ZONCpANyPKJiRJ0UhQwSD5hY0c8jLg/Vir0QCIAAAAADw8KGrg/6p4eSIkBwsoQk0HAqLDF7WfJBgRI4IVAvhLtuLcH/XMChLDprLJRvTOWKranUx9m8QkEQg7Viem5YwiLwdM260ZeJ5MFAoNCMZJCcofw8BwFg23nr561BSGjxb//Se2/////2eEis/23/oybM9JT5kLetTCXkFJL2CCg8DGQqYXgBqKpzBGZeG9BAbwz0Ao6CAILJxBjcOxb/+kapQIVLUav1WZ+rTLEvGtKAO6xZ/XEl9SMWJh0WGRGHs///EB4C3+grX9zWHCg2BhQsNzvlRNnq7uPxbXe/yduXv0Wt8g9ZcT8Pl3KTxd2WaUTwRh+IuEyZUDvnichbsmItgAAAC8JiWY0xQqWESsmAUcEmKuoaNCZqiW264MKQHStjymqm0sZ0NVreCgJshLMgCSoYSUGCunx8nI4tqcPBWu7/+7Rk7AZEaUbTU3hK8ISr6s9hJdJQgSFVrJzagg0tq32XijljpQ2PJlqYS+KJTzucZNj4dLT7DeztSpUeZL1/vbeGR4ik/Bc////Lr/PX/////o5jnU3P/rqVWnns23T4K3mZp5WAAAAAAChM5ZQFLlr0TvSIYgcwwliHCnpS8UNJgbloXxFlDJKvdVGbsjaxDUQwetqEKZK60oSddNlkOQuMPjNMTnn3VIxd2ovhb/wsAWED/mt+WaMsFYYD0VKO/9GlxhvxR1ONGmvvdnvCwrRwe8NNlUPOIk9UFAsgEhQi1e2gfCeZ8Qo/uN7QcNeWISdE95ipeEii9IAAAAAABi808mLUbUC4AQGkhahW1ZKRLFIMGS0JzFHwHgwc8lZASKw8PEnZU4R6QCpzDIyQIIAT6R2hDtPkJIU9fKNVtxGB5F9hMb5hHSSA5ZVcumQ9jbP1vZsvHSjaZ43Ydfzb6EYCjpv6/5m1/////jR5SIK9m+Zl0OvUpmZTqxCXIRyH6yMYcRYUDADAAAALj3Rdj4UyEFXenZKj2dYrZ77tH+H6iHI6jecIX8dgooZpmSY3XLZQ4iR/bNZHOKkUKvM+mbp//iQ1q////+K4QFYdy3P+jzWXFcLDHuXafopqxRlzFigiSaNtm5uyBccIwDJBqKxx/F/8fBEUQVWC1mmDUGYdgIAACMN1NA5aizIuJJv4AOiRU64Uielok4kEyh32MqNUnGhoriUPd6bRLi2soh6pNw4zaQlHK9DzqamHKTP/+7Rk7YBEqmBVa0dGkIsMCr1l5bYPcUFf7D0LwfWwK72HlfiYpzHesGX54sMOEjV4/GF60GKyQnlm089Sywdf234xALf//+lP////6CgeFf/1vIr5y5Wyvo/WgfGu+JCZhip4QEAQAAAASjuYYaAQNFSWZUqBIcgyCFGtMxXU7sXV0v1LdCMWIUsILCkBCpDBZIakF1AZbE3Ahw1WLYakAE2EeYjmkiIPlslx8h+oiQxwyZDyGHhjyInyLjNEQD8zciRcIGO0ul4gpiQdaBmgb00k6yeI8yKhcZN/WukedFNFp1U8q/R1mBqihdAicunKLp6lLLzGJbHAm3/zJBkjLUo1//91pMl5qieloBAAAACkmzJA6KYarUxGGSwbqt9pMCJqMSZ3DCI70A5DWZJJUWki6KchY/w5ESAuRBnJ9yNNDHFFLw6H7BeO4EiUilXbMpjsWtPFa+bEuWG6sVUJ6qoTJi8C8T4k/o9Z2ZSst//SkeW/trer115cebH3/6/5eRa0xuiP29k3Xd/8YtGip26EX1/////mPr5zF+bwtf///////WK7r//GtPIwBQAAAAAABc8BSCScLC4Ydmh0bMTEDUdqQNAmq4gk7mLErpmRiRqhUZOUAQkLQzAWOgUwFAQOgpfScyEFJEyMESLGJZD2ZLVG5K4KjwuWKzptRwhQIvUMYLrCRJfoVGkAJCkxY8MSJxlgW86zkqnzfXZjAhQaTKaREYHMMHREwXy60AXJVqmu6aU3FtXNqOVClOj/+7RE7oAFQmBWfWYAAKEsCt2sPAAiUcVJmb0ABDU36Kc3oACy40SfeM1Y9D0diL+2KtLTy+LU+ojHKF643Lqd9H0jDS4zlWlVWljNZ4I98PXqRy9d+3ajjy4SuB68ORitKseVcspVjj92rY5///3a+34a+5cXa45EUct/4u7kcnJTWppVVxlOWVbeNXn/////////////////////L6/bH//U6AAAAAAAA0I2ZKHg0BBTAIH1qoGBTp0c0JKIzQaHAqFCMAGk4zdHKRg3dbMVHg4iBKoAIQjwOHBGAMSMMtmMe8OZ2C50AqzWGggUghAQU0gExpUyxwyKsQGwuALK1pIYgAAmwGOGIDu0YYMYAsBQ6lQgClumRLqktwmJiwEuarfATqDxEeTP+pk4sMw88NWM1PgVmKcUbhiQz1JWLbPRKqW5jyU3sv+Nxd+pXWeGDI+8dPKt5QPADX6u8f3KX9xbpAXw9RSxr+u/UkjjLdrzsDUtJGOZVcMtZVseanbN/v///cqYUu8t/T6n+YSODuf3/+rKf/5TLce/////////////////////9kP//8jVPVwAACtIjEIgwR4JEYxdQLoByeQ3RDSGivBzJkIaAsliN0hKpUyHOZfRbUKa0NULLRTGkaTixIchzNKfpOSEszCoXGE+nYU6+zWuvaE+1CV0bL2Lh9XG//i1tYt61w+fahPn1lgr/8NFjwiPfywNQVWCp0seEQdiWGgIBxvkSa016XpUmJJqSmstFB1ercn/+7RER4/zzi/H1z3gAHbF2HXsPAAAAAGkAAAAIAAANIAAAARjQ2XtAARYjtLi6P5CjtAbQAkmwwQcomKNbldGg2s+VyuZpU6aLkwoahqtiwk8h0WR8+jZgvXtvXFrbzBt////mv+PmC93BehpP+eyoaLBziJTxKWDgiBpYKjwV//4l6jxZUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVX/+7RkAA/wAABpAAAACAAADSAAAAEAAAGkAAAAIAAANIAAAARMQU1FMy4xMDBVVVVVVVVVVVVVVVVVVVVVVVVVVUxBTUUzLjEwMFVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVU=";

function startVacuumSound(){
  if(vacuumSound)return;

  // 사용자 동작 직후 실행되므로 브라우저의 오디오 재생 허용 조건을 만족합니다.
  unlockAppAudio();

  const audio=new Audio(RECORDED_VACUUM_SOUND);
  audio.loop=true;
  audio.preload='auto';
  audio.volume=0.1;

  vacuumSound={audio};

  try{
    audio.currentTime=0;
  }catch(e){}

  const playPromise=audio.play();
  if(playPromise&&typeof playPromise.catch==='function'){
    playPromise.catch(()=>{
      if(vacuumSound&&vacuumSound.audio===audio)vacuumSound=null;
    });
  }
}

function stopVacuumSound(){
  if(!vacuumSound)return;

  const nodes=vacuumSound;
  vacuumSound=null;

  const audio=nodes.audio;
  if(!audio)return;

  // 청소가 끝나면 녹음 재생만 멈추고, 청소 완료 차임은 기존 로직에서 별도로 재생됩니다.
  try{
    audio.pause();
    audio.currentTime=0;
  }catch(e){}
}

// ============================================================
// 충전 중 효과음
// ============================================================
function startChargingSound(){
  if(chargingSound)return;
  const ctx=getAppAudioContext();
  if(!ctx)return;
  const output=getAppAudioMaster(ctx);

  const master=ctx.createGain();
  master.gain.setValueAtTime(0.0001,ctx.currentTime);
  master.gain.exponentialRampToValueAtTime(0.052,ctx.currentTime+0.28);
  master.connect(output);

  const hum=ctx.createOscillator();
  const humGain=ctx.createGain();
  hum.type='sine';
  hum.frequency.value=82;
  humGain.gain.value=0.36;
  hum.connect(humGain).connect(master);

  const soft=ctx.createOscillator();
  const softGain=ctx.createGain();
  soft.type='triangle';
  soft.frequency.value=164;
  softGain.gain.value=0.065;
  soft.connect(softGain).connect(master);

  const pulse=ctx.createOscillator();
  const pulseGain=ctx.createGain();
  pulse.type='sine';
  pulse.frequency.value=0.72;
  pulseGain.gain.value=0.075;
  pulse.connect(pulseGain).connect(humGain.gain);

  hum.start();
  soft.start();
  pulse.start();
  chargingSound={master,hum,soft,pulse};
}

function stopChargingSound(){
  if(!chargingSound)return;
  const ctx=getAppAudioContext();
  const nodes=chargingSound;
  chargingSound=null;
  if(!ctx)return;
  const t=ctx.currentTime;
  try{
    nodes.master.gain.cancelScheduledValues(t);
    nodes.master.gain.setValueAtTime(Math.max(nodes.master.gain.value,0.0001),t);
    nodes.master.gain.exponentialRampToValueAtTime(0.0001,t+0.24);
  }catch(e){}
  setTimeout(()=>{
    ['hum','soft','pulse'].forEach(k=>{try{nodes[k].stop()}catch(e){}});
    try{nodes.master.disconnect()}catch(e){}
  },280);
}

// ============================================================
// 청소 완료 효과음: 밝은 3음 차임
// ============================================================
function playCleaningCompleteSound(){
  const ctx=getAppAudioContext();
  if(!ctx)return;
  const output=getAppAudioMaster(ctx);
  const now=ctx.currentTime;
  const master=ctx.createGain();
  master.gain.setValueAtTime(0.0001,now);
  master.gain.exponentialRampToValueAtTime(0.105,now+0.012);
  master.gain.exponentialRampToValueAtTime(0.0001,now+0.82);
  master.connect(output);

  const note=(start,freq,duration,vol)=>{
    const osc=ctx.createOscillator();
    const gain=ctx.createGain();
    osc.type='sine';
    osc.frequency.setValueAtTime(freq,start);
    gain.gain.setValueAtTime(0.0001,start);
    gain.gain.exponentialRampToValueAtTime(vol,start+0.010);
    gain.gain.exponentialRampToValueAtTime(0.0001,start+duration);
    osc.connect(gain).connect(master);
    osc.start(start);
    osc.stop(start+duration+0.03);
  };

  note(now,523.25,0.24,0.78);
  note(now+0.16,659.25,0.28,0.70);
  note(now+0.34,783.99,0.36,0.66);
  setTimeout(()=>{try{master.disconnect()}catch(e){}},900);
}

// ============================================================
// 충전 완료 효과음: 부드러운 2음 차임
// ============================================================
function playChargingCompleteSound(){
  const ctx=getAppAudioContext();
  if(!ctx)return;
  const output=getAppAudioMaster(ctx);
  const now=ctx.currentTime;
  const master=ctx.createGain();
  master.gain.setValueAtTime(0.0001,now);
  master.gain.exponentialRampToValueAtTime(0.095,now+0.010);
  master.gain.exponentialRampToValueAtTime(0.0001,now+0.72);
  master.connect(output);

  const note=(start,freq,duration,volume)=>{
    const osc=ctx.createOscillator();
    const gain=ctx.createGain();
    osc.type='sine';
    osc.frequency.setValueAtTime(freq,start);
    gain.gain.setValueAtTime(0.0001,start);
    gain.gain.exponentialRampToValueAtTime(volume,start+0.010);
    gain.gain.exponentialRampToValueAtTime(0.0001,start+duration);
    osc.connect(gain).connect(master);
    osc.start(start);
    osc.stop(start+duration+0.03);
  };

  note(now,659.25,0.26,0.76);
  note(now+0.20,880.00,0.34,0.66);
  setTimeout(()=>{try{master.disconnect()}catch(e){}},800);
}

// ============================================================
// 홈지니 터치 효과음
// ============================================================
function playHomeGenieTouchSound(){
  const ctx=getAppAudioContext();
  if(!ctx)return;
  const output=getAppAudioMaster(ctx);
  const now=ctx.currentTime;
  const master=ctx.createGain();
  master.gain.setValueAtTime(0.0001,now);
  master.gain.exponentialRampToValueAtTime(0.110,now+0.012);
  master.gain.exponentialRampToValueAtTime(0.0001,now+0.34);
  master.connect(output);

  const note=(start,f1,f2,duration,volume)=>{
    const osc=ctx.createOscillator();
    const gain=ctx.createGain();
    osc.type='sine';
    osc.frequency.setValueAtTime(f1,start);
    osc.frequency.exponentialRampToValueAtTime(f2,start+duration);
    gain.gain.setValueAtTime(0.0001,start);
    gain.gain.exponentialRampToValueAtTime(volume,start+0.010);
    gain.gain.exponentialRampToValueAtTime(0.0001,start+duration);
    osc.connect(gain).connect(master);
    osc.start(start);
    osc.stop(start+duration+0.02);
  };

  note(now,660,880,0.12,0.88);
  note(now+0.105,900,1180,0.16,0.78);
  setTimeout(()=>{try{master.disconnect()}catch(e){}},420);
}

document.addEventListener('pointerdown',unlockAppAudio,{once:true,capture:true});
document.addEventListener('touchstart',unlockAppAudio,{once:true,capture:true,passive:true});

// ============================================================
// 배터리 보호/학습 주행 기준값
// 최근 UX 문구 수정 과정에서 이 상수들이 빠지면
// 1회차 학습 버튼 클릭 시 startFirstMapping() 내부에서 ReferenceError가 발생합니다.
// 그래서 사용자에게 숫자를 직접 노출하지 않더라도, 내부 로직에는 반드시 유지합니다.
// ============================================================
const MIN_RESERVE_SOC = 15;
const MAX_CHARGE_SOC = 90;
const MAX_SINGLE_PASS_USE = MAX_CHARGE_SOC - MIN_RESERVE_SOC;
const CRITICAL_DOCK_SOC = MIN_RESERVE_SOC;
const targetFromRequired = (required)=>clamp(Math.ceil(Number(required||0)+MIN_RESERVE_SOC),MIN_RESERVE_SOC,MAX_CHARGE_SOC);
const expectedEndSoc = (startSoc,required)=>Math.round((Number(startSoc||0)-Number(required||0))*10)/10;

const MIN_SOC_AFTER_LEARNING = MIN_RESERVE_SOC;
const MIN_LEARNING_SOC_USE = 5;
const MAX_LEARNING_SOC_USE = 30;
const LEARNING_SOC_RATIO = 0.35;

// 시연용: 이전에 이미 몇 번 청소한 로봇처럼 보이게 하는 누적 청소 횟수 기준값
// (미션 "10번 청소하기"가 시연 중 첫 청소로 달성되도록 9로 둡니다)
const DEMO_CLEAN_BASE = 9;

function setModeChipText(text){
  const el=$("modeChip");
  if(el)el.textContent=text;
}

function setGuide(message,tone="normal"){
  state.userGuide=message;
  state.userGuideTone=tone;
  const guide=$('flowGuide');
  if(guide){
    guide.className="flow-guide"+(tone&&tone!=="normal"?" "+tone:"");
    guide.innerHTML="<span class='guide-step'>다음 안내</span>"+message;
  }
}
function guideForCurrentState(){
  if(state.mapping)return "홈지니가 우리 집을 배우는 중이에요. 집 구조와 바닥 상태를 차근차근 기억하고 있어요.";
  if(!state.profileReady)return "<b>1단계</b> 먼저 1회차 학습 청소로 우리 집을 알려주세요.";
  if(state.profileReady && !state.predicted)return "<b>2단계</b> AI 자동청소를 고르거나, 바로 청소하기를 눌러주세요.";
  if(state.charging)return "홈지니가 잠깐 쉬면서 힘을 채우고 있어요. 필요한 만큼 채우면 알아서 멈춰요.";
  if(state.cleaning)return "청소 중이에요. 배터리가 무리하지 않도록 홈지니가 알아서 조절하고 있어요.";
  if(state.celebrating || state.missionDone)return "청소가 끝났어요! 홈지니가 배터리를 아끼며 마무리했어요.";
  if(state.predicted && state.soc<state.targetSoc)return "<b>3단계</b> 준비가 끝났어요. 청소하기를 누르면 필요한 만큼만 채우고 출발해요.";
  if(state.predicted)return "<b>3단계</b> 지금 바로 출동할 수 있어요. 청소하기를 눌러주세요.";
  return state.userGuide||"현재 상태를 확인 중입니다.";
}

function getLearningSocUse(run,startSoc){
  const fullRequired=Math.max(0,Number(run&&run.home?run.home.requiredSoc:0));
  const available=Math.max(0,Number(startSoc||0)-MIN_SOC_AFTER_LEARNING);
  if(fullRequired<=0 || available<=0)return 0;
  let mappedUse=fullRequired*LEARNING_SOC_RATIO;
  mappedUse=Math.max(MIN_LEARNING_SOC_USE,mappedUse);
  mappedUse=Math.min(mappedUse,MAX_LEARNING_SOC_USE,fullRequired,available);
  return Math.round(mappedUse*10)/10;
}

const cleanModeLabels={dry:"건식",mop:"물걸레",both:"건식+물걸레"};
const intensityLabels={fast:"빠른",standard:"표준",careful:"꼼꼼"};
const todayStateLabels={normal:"평소와 같음",dust:"먼지 많음",pet:"반려동물 털 많음",obstacle:"바닥 물건 많음"};
// 아래 선택값은 배율을 곱하는 보정계수가 아니라,
// 기록 안에서 조건이 가장 가까운 우리 집 기록 준비 행을 찾기 위한 검색 조건으로 사용됩니다.
const intensityAliases={fast:["약","중"],standard:["중","강"],careful:["강","터보"]};
const todayStateAliases={normal:"학습 프로필 기준",dust:"오염도 높은 조건",pet:"오염도 높음 + 강한 흡입 조건",obstacle:"장애물 많은 조건"};

const closetDefault={
  owned:{santa:false,ribbon:false,hat:false,bunny:false,cat:false,sparkle:false},
  equipped:{head:"crown",aura:null}
};
const shopItems={
  santa:{name:"산타클로스 모자",icon:"🎄",cost:50,slot:"head",value:"santa",message:"메리 크리스마스! 산타 모자를 씌워 홈지니가 크리스마스 에디션으로 변신했어요."},
  ribbon:{name:"빨간 리본",icon:"🎀",cost:60,slot:"head",value:"ribbon",message:"빨간 리본을 달아줬어요! 홈지니가 더 사랑스러워졌어요."},
  hat:{name:"탐험가 모자",icon:"🧢",cost:120,slot:"head",value:"hat",message:"탐험가 모자를 씌워줬어요! 이제 진짜 모험가 홈지니가에요."},
  bunny:{name:"토끼 귀",icon:"🐰",cost:90,slot:"head",value:"bunny",message:"토끼 귀를 달아줬어요! 홈지니가 통통 튀는 기분이에요."},
  cat:{name:"고양이 귀",icon:"🐱",cost:70,slot:"head",value:"cat",message:"고양이 귀를 달아줬어요! 홈지니가 더 새침해졌어요."},
  sparkle:{name:"반짝이 오라",icon:"✨",cost:80,slot:"aura",value:"sparkle",message:"반짝이 오라를 켰어요! 청소할 때마다 기분이 좋아져요."}
};

const couponItems={
  lg5:{name:"LG 생활가전 5% 쿠폰",icon:"🎟",cost:300,benefit:"LG 생활가전 1개 구매 시 5% 할인",message:"LG 생활가전 5% 쿠폰을 보관함에 담았어요."},
  cleanKit:{name:"홈지니 클린 키트 쿠폰",icon:"🧹",cost:180,benefit:"필터·브러시·물걸레 패드 등 소모품 키트 할인",message:"홈지니 클린 키트 쿠폰을 보관함에 담았어요."},
  batteryCare:{name:"배터리 케어 쿠폰",icon:"🔋",cost:250,benefit:"배터리 점검 또는 관리 서비스 혜택",message:"배터리 케어 쿠폰을 보관함에 담았어요."},
  moveIn:{name:"제휴 OTT 50% 할인 쿠폰",icon:"📺",cost:300,benefit:"넷플릭스·디즈니플러스·유튜브 프리미엄 등 제휴 OTT 첫 달 50% 할인",message:"제휴 OTT 50% 할인 쿠폰을 보관함에 담았어요."}
};
function loadCoupons(){
  try{
    const raw=localStorage.getItem("lgRoboCareCouponsV1");
    const defaults={lg5:0,cleanKit:0,batteryCare:0,moveIn:0};
    if(!raw)return defaults;
    return Object.assign(defaults,JSON.parse(raw)||{});
  }catch(e){return {lg5:0,cleanKit:0,batteryCare:0,moveIn:0};}
}
function saveCoupons(){
  try{localStorage.setItem("lgRoboCareCouponsV1",JSON.stringify(state.ownedCoupons));}catch(e){}
}

// 홈지니 첫 사용일을 브라우저에 저장해 배터리 케어 화면의 D+ 사용일을 계산합니다.
// 실제 제품 연동 시에는 localStorage 대신 제품 등록일/최초 활성화일을 연결하면 됩니다.
function localDateString(date){
  const y=date.getFullYear();
  const m=String(date.getMonth()+1).padStart(2,"0");
  const d=String(date.getDate()).padStart(2,"0");
  return y+"-"+m+"-"+d;
}
function loadFirstUseDate(){
  const key="lgRoboCareFirstUseDateV1";
  try{
    let saved=localStorage.getItem(key);
    if(saved && /^\d{4}-\d{2}-\d{2}$/.test(saved))return saved;
    saved=localDateString(new Date());
    localStorage.setItem(key,saved);
    return saved;
  }catch(e){
    return localDateString(new Date());
  }
}
const firstUseDate=loadFirstUseDate();
function getUsageDayCount(){
  const first=new Date(firstUseDate+"T00:00:00");
  const now=new Date();
  const today=new Date(now.getFullYear(),now.getMonth(),now.getDate());
  if(Number.isNaN(first.getTime()))return 1;
  return Math.max(1,Math.floor((today-first)/86400000)+1);
}
function formatFirstUseDate(){
  const parts=firstUseDate.split("-");
  return parts.length===3 ? parts[0]+"."+parts[1]+"."+parts[2] : firstUseDate;
}

function loadCloset(){
  try{
    const raw=localStorage.getItem("lgRoboCareClosetV2");
    if(!raw)return JSON.parse(JSON.stringify(closetDefault));
    const saved=JSON.parse(raw);
    const owned=Object.assign({},closetDefault.owned,saved.owned||{});
    // 이전 버전에서 하트 스티커를 샀다면 고양이 귀 보유로 자연스럽게 이전합니다.
    if(saved.owned && saved.owned.heart && !owned.cat)owned.cat=true;
    const equipped=Object.assign({},closetDefault.equipped,saved.equipped||{});
    if(equipped.decal==="heart" && (!equipped.head || equipped.head==="crown"))equipped.head="cat";
    delete equipped.decal;
    return {owned,equipped};
  }catch(e){return JSON.parse(JSON.stringify(closetDefault));}
}
function saveCloset(){
  try{localStorage.setItem("lgRoboCareClosetV2",JSON.stringify({owned:state.ownedItems,equipped:state.equippedItems}));}catch(e){}
}
const initialCloset=loadCloset();
const initialCoupons=loadCoupons();

function getBatteryWeekKey(date=new Date()){
  const d=new Date(Date.UTC(date.getFullYear(),date.getMonth(),date.getDate()));
  const day=d.getUTCDay()||7;
  d.setUTCDate(d.getUTCDate()+4-day);
  const yearStart=new Date(Date.UTC(d.getUTCFullYear(),0,1));
  const week=Math.ceil((((d-yearStart)/86400000)+1)/7);
  return d.getUTCFullYear()+"-W"+String(week).padStart(2,"0");
}
function loadBatteryStrategy(){
  try{
    const v=localStorage.getItem("lgRoboCareBatteryStrategyV1");
    return v==="ready"?"ready":"care";
  }catch(e){return "care";}
}
function saveBatteryStrategy(){
  try{localStorage.setItem("lgRoboCareBatteryStrategyV1",state.batteryStrategy);}catch(e){}
}
function loadWeeklyBatteryHabit(){
  const weekKey=getBatteryWeekKey();
  try{
    const raw=localStorage.getItem("lgRoboCareWeeklyBatteryHabitV1");
    if(raw){
      const saved=JSON.parse(raw)||{};
      if(saved.weekKey===weekKey){
        return {weekKey,smartCharge:Number(saved.smartCharge||0),reserveGuard:Number(saved.reserveGuard||0)};
      }
    }
  }catch(e){}
  // 시연 초기값: 기존 배터리 케어 누적값과 자연스럽게 연결합니다.
  return {weekKey,smartCharge:4,reserveGuard:1};
}
function saveWeeklyBatteryHabit(){
  try{localStorage.setItem("lgRoboCareWeeklyBatteryHabitV1",JSON.stringify(state.weeklyBatteryHabit));}catch(e){}
}
function ensureWeeklyBatteryHabit(){
  const key=getBatteryWeekKey();
  if(!state.weeklyBatteryHabit || state.weeklyBatteryHabit.weekKey!==key){
    state.weeklyBatteryHabit={weekKey:key,smartCharge:0,reserveGuard:0};
    saveWeeklyBatteryHabit();
  }
  return state.weeklyBatteryHabit;
}
const initialBatteryStrategy=loadBatteryStrategy();
const initialWeeklyBatteryHabit=loadWeeklyBatteryHabit();

function pickRandomRun(candidates){
  if(!candidates || candidates.length===0)return null;

  // 현재 화면에 떠 있는 global_run_id와 같은 시나리오는 가능하면 제외
  // 같은 조건으로 1회차 학습 청소를 다시 실행할 때 매번 다른 집 정보가 나오게 하기 위함
  let pool = candidates;
  if(activeRun && activeRun.globalRunId && candidates.length>1){
    const filtered = candidates.filter(r=>String(r.globalRunId)!==String(activeRun.globalRunId));
    if(filtered.length>0)pool = filtered;
  }

  const idx = Math.floor(Math.random()*pool.length);
  return pool[idx];
}

function findRun(areaPyung, mopEnabled){
  const area = Number(areaPyung);
  const mop = Boolean(mopEnabled);

  // 1순위: 사용자가 선택한 평수 + 청소방식이 모두 같은 기록 시나리오 중 랜덤 선택
  let candidates = predictionData.runs.filter(r=>Number(r.areaPyung)===area && Boolean(r.mopEnabled)===mop);
  let run = pickRandomRun(candidates);

  // 2순위: 청소방식까지 완전히 맞는 데이터가 없으면, 같은 평수 안에서 랜덤 선택
  if(!run){
    candidates = predictionData.runs.filter(r=>Number(r.areaPyung)===area);
    run = pickRandomRun(candidates);
  }

  // 3순위: 같은 평수도 없으면 전체 기록 중 랜덤 선택
  if(!run){
    run = pickRandomRun(predictionData.runs);
  }

  return run || predictionData.runs[0];
}

activeRun = pickRandomRun(predictionData.runs) || predictionData.runs[0];

const state={
  page:"homePage",
  soc:predictionData.currentSoc,
  targetSoc:activeRun.home.targetSoc,
  requiredSoc:activeRun.home.requiredSoc,
  selectedScope:"home",
  selectedZone:null,
  selectedLabel:activeRun.home.label,
  selectedScenario:activeRun.home,
  modelName:activeRun.home.modelName,
  globalRunId:activeRun.home.globalRunId,
  areaPyung:activeRun.home.areaPyung,
  cleaningAreaM2:activeRun.home.cleaningAreaM2,
  cleaningType:activeRun.home.cleaningType,
  mopEnabled:activeRun.home.mopEnabled,
  obstacleLevel:activeRun.home.obstacleLevel,
  floorType:activeRun.home.floorType,
  dirtLevel:activeRun.home.dirtLevel,
  suctionMode:activeRun.home.suctionMode,
  cleanModeChoice:activeRun.home.mopEnabled?'mop':'dry',
  cleanModeLabel:activeRun.home.cleaningType,
  intensityChoice:'standard',
  intensityLabel:'표준',
  todayStateChoice:'normal',
  todayStateLabel:'평소와 같음',
  matchNote:"우리 집 기록으로 맞춤 준비",
  matchBasis:"오늘 상태 반영",
  cleaningRemainingSoc:activeRun.home.requiredSoc,
  cleaningSegmentIndex:0,
  splitCleaning:false,
  pendingCleanAfterCharge:false,
  chargeComplete:false,
  predicting:false,
  predicted:false,
  userGuide:"1회차 학습 청소로 집 크기, 구역, 바닥, 오염도, 배터리 사용을 저장해 주세요.",
  userGuideTone:"normal",
  profileReady:false,
  mapping:false,
  mappingProgress:0,
  mappingStepIndex:-1,
  firstRunSocUsed:0,
  firstRunRequiredSoc:0,
  firstRunFullRequiredSoc:0,
  firstRunStartSoc:predictionData.currentSoc,
  firstRunEndSoc:predictionData.currentSoc,
  firstRunSocEnough:true,
  ownedItems:initialCloset.owned,
  equippedItems:initialCloset.equipped,
  rewardTab:"items",
  ownedCoupons:initialCoupons,
  noGoZones:[],
  mapMode:"view",
  smartCleanMode:"auto",
  batteryStrategy:initialBatteryStrategy,
  weeklyBatteryHabit:initialWeeklyBatteryHabit,
  selectedDirtyZones:[],
  manualReady:false,
  manualKey:"",
  robotMotion:"idle",
  cleaningZones:[],
  currentCleaningZone:null,
  completedZones:[],
  cleanAnim:null,
  chargePurpose:"current",
  nextHomeReady:false,
  nextHomeTargetSoc:0,
  nextHomeRequiredSoc:0,
  temperature:29,health:100,heart:100,
  level:13,exp:55,coins:50,food:1,cleaning:false,charging:false,
  celebrating:false,progress:0,missionDone:false,cleanCount:0,
  acceptCount:4,area:activeRun.home.cleaningAreaM2||72,average:38,

  // ---- 새 페이지(부품 케어 / 예약 청소 / 이벤트) 전용 상태 ----
  learnCount:0,
  savedChargePct:76,
  reserveGuardCount:1,
  claimedMissions:{},
  notifiedClaimable:0,
  eventTab:"found",
  commuteOn:false,
  commuteDays:[1,2,3,4,5],
  commuteMode:"after",
  activeThemes:{}
};

function populateConditionSelectors(){
  refreshScopeSelect();
  const cleanModeSelect=$('cleanModeSelect');
  if(cleanModeSelect)cleanModeSelect.value=activeRun.mopEnabled?'mop':'dry';
  const scopeSelect=$('scopeSelect');
  if(scopeSelect)scopeSelect.value='home';
  const intensitySelect=$('intensitySelect');
  if(intensitySelect)intensitySelect.value='standard';
  const todayStateSelect=$('todayStateSelect');
  if(todayStateSelect)todayStateSelect.value='normal';
}

function switchPage(pageId){
  if(!$(pageId))return;
  document.querySelectorAll(".page").forEach(p=>p.classList.remove("active"));
  document.querySelectorAll(".nav-btn").forEach(b=>b.classList.toggle("active",b.dataset.page===pageId));
  $(pageId).classList.add("active");
  state.page=pageId;
  render();
}

function render(){
  state.soc=clamp(Math.round(state.soc),0,100);
  state.targetSoc=clamp(Math.round(state.targetSoc),15,90);
  state.temperature=Math.round(state.temperature*10)/10;
  state.exp=clamp(Math.round(state.exp),0,100);

  $("coinText").textContent=String(state.coins).padStart(3,"0");
  $("foodText").textContent=state.food;
  $("cleanTime").textContent=cleanMinutes();
  $("pointer").style.left=state.soc+"%";
  $("cleanFill").style.width=state.progress+"%";
  $("missionFill").style.width=state.missionDone?"100%":state.progress+"%";
  const robotSocBadge=$("robotSocBadge");
  if(robotSocBadge){
    const socState=state.soc<15?"low":(state.soc<state.targetSoc?"need":"ok");
    robotSocBadge.className="robot-soc-badge "+socState;
    robotSocBadge.innerHTML="<button type=\"button\" class=\"battery-help-btn\" data-action=\"batteryCoachInfo\" aria-label=\"배터리 코칭 안내 보기\">!</button><span>🔋 현재 배터리</span><b>"+state.soc+"%</b>";
  }

  renderAccessories();renderPlan();renderHome();
  renderCare();renderSchedule();renderEvents();
  renderReward();
}

function getScenario(scope,zoneNumber=null){
  if(scope==="home")return activeRun.home;
  const zones=(activeRun && activeRun.zones) ? activeRun.zones : [];
  const direct=zones.find(z=>Number(z.zone)===Number(zoneNumber)) || zones[zoneNumber-1];
  if(direct)return direct;

  // 혹시 예전 CSV/캐시로 해당 영역 데이터가 아직 없으면 가장 가까운 영역 데이터를 임시로 사용합니다.
  // 새 4/6/8구역 CSV로 교체되면 실제 해당 영역 데이터가 자동으로 잡힙니다.
  if(zones.length){
    const idx=Math.min(Math.max(Number(zoneNumber||1)-1,0),zones.length-1);
    return zones[idx];
  }
  return activeRun.home;
}

function getPredictionChoices(scopeOverride=null,zoneOverride=null){
  const scopeSelect=$('scopeSelect');
  const cleanModeSelect=$('cleanModeSelect');
  const intensitySelect=$('intensitySelect');
  const todayStateSelect=$('todayStateSelect');
  const scopeValue=scopeOverride? (scopeOverride==="home"?"home":String(zoneOverride||1)) : (scopeSelect?scopeSelect.value:"home");
  return {
    scopeValue,
    scope:scopeValue==="home"?"home":"zone",
    zoneNumber:scopeValue==="home"?null:Number(scopeValue),
    cleanMode:cleanModeSelect?cleanModeSelect.value:(activeRun.home.mopEnabled?'mop':'dry'),
    intensity:intensitySelect?intensitySelect.value:'standard',
    todayState:todayStateSelect?todayStateSelect.value:'normal'
  };
}

function getBaseScenarioFromChoices(choices){
  if(choices.scope==="home")return activeRun.home;
  return getScenario("zone",choices.zoneNumber);
}

function getCleanModeCandidateValue(scenario){
  const txt=String(scenario.cleaningType||"");
  if(txt.includes("건식+물걸레")||txt.includes("복합")||txt.includes("both"))return "both";
  if(scenario.mopEnabled || txt.includes("물걸레") || txt.toLowerCase().includes("mop"))return "mop";
  return "dry";
}

function cleanModeScore(scenario,choice){
  const v=getCleanModeCandidateValue(scenario);
  if(choice===v)return 120;
  // 데이터셋에 건식+물걸레가 없을 수 있으므로, 복합 청소는 물걸레 조건을 가장 가까운 후보로 인정합니다.
  if(choice==="both" && v==="mop")return 70;
  return -260;
}

function suctionPreferenceScore(scenario,intensity){
  const mode=String(scenario.suctionMode||"");
  const code=Number(scenario.suctionCode||scenario.suctionMaxCode||0);
  if(intensity==="fast"){
    if(mode.includes("약"))return 80;
    if(mode.includes("중"))return 50;
    if(code && code<=2)return 60;
    return -25;
  }
  if(intensity==="careful"){
    if(mode.includes("터보"))return 90;
    if(mode.includes("강"))return 65;
    if(code && code>=3)return 70;
    return -20;
  }
  // 표준은 중/강 또는 학습 프로필과 가까운 후보를 우선합니다.
  if(mode.includes("중"))return 70;
  if(mode.includes("강"))return 45;
  if(code && code>=2 && code<=3)return 55;
  return 10;
}

function todayStateScore(scenario,choice,baseScenario){
  const dirt=Number(scenario.dirtCode||scenario.dirtMaxCode||0);
  const dirtMax=Number(scenario.dirtMaxCode||dirt||0);
  const obs=Number(scenario.obstacleLevelCode||0);
  const suction=Number(scenario.suctionCode||scenario.suctionMaxCode||0);
  const mode=String(scenario.suctionMode||"");
  const baseDirt=Number(baseScenario.dirtCode||baseScenario.dirtMaxCode||0);
  const baseObs=Number(baseScenario.obstacleLevelCode||0);

  if(choice==="dust"){
    if(dirtMax>=3 || dirt>=3 || String(scenario.dirtLevel||"").includes("높"))return 100;
    if(dirt>=2)return 45;
    return -20;
  }
  if(choice==="pet"){
    let score=0;
    if(dirtMax>=3 || dirt>=3 || String(scenario.dirtLevel||"").includes("높"))score+=60;
    if(suction>=3 || mode.includes("강") || mode.includes("터보"))score+=60;
    return score || -20;
  }
  if(choice==="obstacle"){
    if(obs>=3 || String(scenario.obstacleLevel||"").includes("높"))return 100;
    if(obs>=2 || String(scenario.obstacleLevel||"").includes("중"))return 45;
    return -20;
  }
  // 평소와 같음은 1회차 학습 프로필의 오염도/장애물 수준과 가까운 후보를 우선합니다.
  return 70 - Math.abs((dirt||baseDirt)-baseDirt)*12 - Math.abs((obs||baseObs)-baseObs)*12;
}

function scenarioPoolForChoices(choices){
  if(!predictionData.runs || !predictionData.runs.length)return [];
  if(choices.scope==="home"){
    return predictionData.runs.map(r=>r.home).filter(Boolean);
  }
  const zoneNo=Number(choices.zoneNumber||1);
  const pool=[];
  predictionData.runs.forEach(r=>{
    const z=(r.zones||[]).find(item=>Number(item.zone)===zoneNo);
    if(z)pool.push(z);
  });
  return pool;
}

function scoreScenarioForChoices(scenario,choices,baseScenario){
  let score=0;
  score+=cleanModeScore(scenario,choices.cleanMode);
  score+=suctionPreferenceScore(scenario,choices.intensity);
  score+=todayStateScore(scenario,choices.todayState,baseScenario);

  // 1회차 학습한 우리 집 정보과 최대한 가까운 후보를 우선합니다.
  if(Number(scenario.areaPyung)===Number(activeRun.home.areaPyung))score+=180;
  else score-=Math.abs(Number(scenario.areaPyung||0)-Number(activeRun.home.areaPyung||0))*4;

  if(choices.scope==="zone"){
    if(Number(scenario.zone)===Number(choices.zoneNumber))score+=80;
    if(baseScenario.floorType && scenario.floorType===baseScenario.floorType)score+=90;
    else if(baseScenario.floorType && scenario.floorType)score-=35;
    score-=Math.abs(Number(scenario.cleaningAreaM2||0)-Number(baseScenario.cleaningAreaM2||0))*1.5;
  }else{
    score-=Math.abs(Number(scenario.cleaningAreaM2||0)-Number(activeRun.home.cleaningAreaM2||0))*.25;
  }

  // 동점 방지를 위한 아주 작은 랜덤값. 조건 점수 자체에는 영향이 거의 없습니다.
  score+=Math.random()*0.01;
  return score;
}

function findMlScenarioFromChoices(choices){
  const baseScenario=getBaseScenarioFromChoices(choices);
  const pool=scenarioPoolForChoices(choices);
  if(!pool.length){
    const fallback=Object.assign({},baseScenario);
    fallback.matchNote="저장된 우리 집 기록으로 준비";
    return fallback;
  }

  let best=null;
  let bestScore=-Infinity;
  pool.forEach(candidate=>{
    const score=scoreScenarioForChoices(candidate,choices,baseScenario);
    if(score>bestScore){bestScore=score;best=candidate;}
  });

  const scenario=Object.assign({},best||baseScenario);
  scenario.scope=choices.scope;
  if(choices.scope==="zone"){
    scenario.zone=Number(choices.zoneNumber||scenario.zone||1);
    scenario.label=scenario.zone+"구역";
  }else{
    scenario.label="집 전체";
  }
  scenario.cleanModeChoice=choices.cleanMode;
  scenario.cleanModeLabel=cleanModeLabels[choices.cleanMode]||scenario.cleaningType;
  scenario.intensityChoice=choices.intensity;
  scenario.intensityLabel=intensityLabels[choices.intensity]||"표준";
  scenario.todayStateChoice=choices.todayState;
  scenario.todayStateLabel=todayStateLabels[choices.todayState]||"평소와 같음";
  scenario.targetSoc=targetFromRequired(scenario.requiredSoc);
  scenario.matchNote="오늘 상태에 맞춰 홈지니가 준비";
  scenario.matchBasis="청소 방식·오염도·장애물 상태 반영";

  if(choices.cleanMode==="both" && getCleanModeCandidateValue(scenario)!=="both"){
    scenario.matchNote="비슷한 청소 기록으로 준비";
  }
  return scenario;
}

function syncScenarioToState(scenario){
  state.selectedScenario=scenario;
  state.selectedScope=scenario.scope;
  state.selectedZone=scenario.scope==="zone"?scenario.zone:null;
  state.selectedLabel=scenario.label;
  state.requiredSoc=Number(scenario.requiredSoc);
  state.targetSoc=Number(scenario.targetSoc);
  state.modelName=scenario.modelName;
  state.globalRunId=scenario.globalRunId;
  state.areaPyung=scenario.areaPyung;
  state.cleaningAreaM2=scenario.cleaningAreaM2;
  state.cleaningType=scenario.cleaningType;
  state.mopEnabled=Boolean(scenario.mopEnabled);
  state.obstacleLevel=scenario.obstacleLevel;
  state.floorType=scenario.floorType;
  state.dirtLevel=scenario.dirtLevel;
  state.suctionMode=scenario.suctionMode;
  state.cleanModeChoice=scenario.cleanModeChoice||state.cleanModeChoice;
  state.cleanModeLabel=scenario.cleanModeLabel||scenario.cleaningType||state.cleaningType;
  state.intensityChoice=scenario.intensityChoice||state.intensityChoice;
  state.intensityLabel=scenario.intensityLabel||state.intensityLabel;
  state.todayStateChoice=scenario.todayStateChoice||state.todayStateChoice;
  state.todayStateLabel=scenario.todayStateLabel||state.todayStateLabel;
  state.matchNote=scenario.matchNote||"우리 집 기록으로 맞춤 준비";
  state.matchBasis=scenario.matchBasis||"오늘 상태 반영";
  state.cleaningRemainingSoc=Number(state.requiredSoc||0);
  state.cleaningSegmentIndex=0;
  state.splitCleaning=state.requiredSoc>MAX_SINGLE_PASS_USE;
  state.progress=0;
  state.missionDone=false;
  state.area=scenario.cleaningAreaM2||state.area;
}

function getManualSelectionKey(){
  const c=getPredictionChoices();
  return [c.scopeValue,c.cleanMode,c.intensity,c.todayState].join("|");
}

function predictSocFromConditions(autoExecuteAfter=false){
  if(state.cleaning||state.charging||state.mapping){showToast("학습/청소/충전이 끝난 뒤 다시 준비할 수 있어요.");return}

  if(!state.profileReady){
    setGuide("아직 홈지니가 우리 집을 잘 몰라요. 먼저 1회차 학습 청소를 시작해 주세요.","warning");
    showToast("먼저 홈지니에게 우리 집을 알려주세요.");
    $("speech").innerHTML="<strong style='color:#ef8c32'>아직 학습 전이에요!</strong><br>먼저 우리 집을 알려주세요.";
    setModeChipText("🏠 1회차 학습 필요");
    switchPage("homePage");
    return;
  }
  const choices=getPredictionChoices();
  const currentManualKey=getManualSelectionKey();
  const matchedScenario=findMlScenarioFromChoices(choices);
  const loading=$('predictLoading');
  state.predicting=true;
  if(loading){loading.textContent="홈지니가 오늘 청소를 준비하고 있어요...";loading.classList.add('active');}
  $("speech").innerHTML="<strong style='color:#2f8b3a'>잠깐만요!</strong><br>오늘 청소 준비를 하고 있어요.";
  setModeChipText("🤖 우리 집 기록으로 준비 중");
  setGuide("오늘 상태를 보고 홈지니가 청소 준비를 하고 있어요. 잠시만 기다려 주세요.","charging");
  showToast("청소 준비 중: 오늘 상태에 맞춰 준비하고 있어요.");

  setTimeout(()=>{
    syncScenarioToState(matchedScenario);
    state.smartCleanMode="manual";
    state.mapMode="view";
    state.selectedDirtyZones=[];
    state.cleaningZones=getCleaningZonesForCurrentPlan();
    state.completedZones=[];
    state.currentCleaningZone=null;
    state.manualReady=true;
    state.manualKey=currentManualKey;
    state.predicted=true;
    state.predicting=false;
    state.chargeComplete=false;
    if(loading){
      const status=state.soc>=state.targetSoc?"바로 청소 가능":"충전 필요";
      loading.textContent="준비 완료 · "+status+" · 홈지니가 필요한 만큼 준비했어요.";
      loading.classList.remove('active');
    }
    render();
    const statusText=state.soc>=state.targetSoc?"바로 청소할 수 있어요":"잠깐 충전하면 청소할 수 있어요";
    $("speech").innerHTML="<strong style='color:#2f8b3a'>준비 완료!</strong><br>"+statusText;
    setModeChipText("✅ 청소 준비 완료 · "+state.selectedLabel);
    addEvent("청소 준비 완료",state.selectedLabel+" 청소에 필요한 만큼만 배터리를 준비했어요.","맞춤 관리");
    setGuide(statusText.includes("바로")?"준비 완료! 바로 출동할게요.":"준비 완료! 필요한 만큼만 채우고 바로 출발할게요.", state.soc>=state.targetSoc?"done":"warning");
    showToast("청소 준비 완료! 홈지니가 오늘 청소 준비를 마쳤어요.");
    if(autoExecuteAfter){
      setTimeout(()=>executeTopClean(),260);
    }
  },900);
}

function floorSummary(){
  if(!activeRun || !activeRun.zones)return "정보 없음";
  const counts={};
  activeRun.zones.forEach(z=>{const k=z.floorType||"정보 없음";counts[k]=(counts[k]||0)+1;});
  return Object.keys(counts).map(k=>k+" "+counts[k]+"구역").join(", ");
}
function floorKindCount(){
  if(!activeRun || !activeRun.zones)return 0;
  const kinds={};
  activeRun.zones.forEach(z=>{kinds[z.floorType||"정보 없음"]=true;});
  return Object.keys(kinds).length;
}
function dirtSummaryShort(){
  if(!activeRun || !activeRun.zones)return "정보 없음";
  const high=activeRun.zones.filter(z=>String(z.dirtLevel||"").includes("높")).length;
  const mid=activeRun.zones.filter(z=>String(z.dirtLevel||"").includes("중") || String(z.dirtLevel||"").includes("보통")).length;
  if(high>0)return "높음 "+high+"구역"+(mid>0?" · 보통 "+mid+"구역":"");
  if(mid>0)return "보통 "+mid+"구역";
  return dirtSummary();
}
function dirtSummary(){
  if(!activeRun || !activeRun.zones)return "정보 없음";
  const counts={};
  activeRun.zones.forEach(z=>{const k=z.dirtLevel||"정보 없음";counts[k]=(counts[k]||0)+1;});
  return Object.keys(counts).map(k=>k+" "+counts[k]+"구역").join(", ");
}
function obstacleSummary(){return activeRun && activeRun.home ? (activeRun.home.obstacleLevel||"중간") : "중간";}
function profileResultBody(){
  return "<b>우리 집 저장 완료</b><br><br>"
    +"집 크기: <b>"+activeRun.areaPyung+"평 · "+activeRun.home.cleaningAreaM2+"㎡</b><br>"
    +"구역: <b>"+getDisplayZoneCount()+"개</b><br>"
    +"바닥: <b>"+floorKindCount()+"종 혼합</b><br>"
    +"오염도: <b>"+dirtSummaryShort()+"</b><br>"
    +"장애물: <b>"+obstacleSummary()+"</b><br>"
    +"배터리를 무리하지 않도록 여유 잔량을 남기며 학습을 마쳤어요.<br><br>"
    +"다음 단계: <b>오늘 청소 준비하기</b>";
}
function startFirstMapping(){
  state.chargePurpose='current';state.nextHomeReady=false;
  if(state.cleaning||state.charging||state.mapping){showToast("진행 중인 작업이 끝난 뒤 다시 시도해 주세요.");return}

  const startSoc=clamp(Math.round(Number(state.soc||0)),0,100);
  if(startSoc < MIN_SOC_AFTER_LEARNING + MIN_LEARNING_SOC_USE){
    openModal("학습 전에 잠깐 충전할게요","처음 우리 집을 배우려면<br>홈지니에게 힘이 조금 더 필요해요.<br><br>잠깐 충전한 뒤 시작하면<br>집 구조를 더 안정적으로 배울 수 있어요.");
    return;
  }

  // 현재 배터리 기준으로 학습 주행 후 여유 배터리를 남길 수 있는 기록 시나리오를 우선 선택합니다.
  const safeRuns=predictionData.runs.filter(r=>getLearningSocUse(r,startSoc)>0);
  activeRun=pickRandomRun(safeRuns.length?safeRuns:predictionData.runs) || predictionData.runs[0];
  syncScenarioToState(activeRun.home);
  refreshScopeSelect();

  const fullRequiredSoc=Number(activeRun.home.requiredSoc||0);
  const learningUse=getLearningSocUse(activeRun,startSoc);
  const expectedEndSoc=Math.max(MIN_SOC_AFTER_LEARNING,startSoc-learningUse);

  state.profileReady=false;
  state.predicted=false;
  state.mapping=true;
  startVacuumSound();
  state.mappingProgress=0;
  state.mappingStepIndex=0;
  state.firstRunFullRequiredSoc=fullRequiredSoc;
  state.firstRunRequiredSoc=learningUse;
  state.firstRunSocUsed=learningUse;
  state.firstRunStartSoc=startSoc;
  state.firstRunEndSoc=expectedEndSoc;
  state.firstRunSocEnough=true;
  state.soc=startSoc;
  state.chargeComplete=false;
  state.celebrating=false;
  switchPage("homePage");
  setGuide("학습 청소를 시작했어요. 홈지니가 우리 집 구조와 바닥 상태를 차근차근 기억하고 있어요.","charging");
  showToast("학습 시작: 홈지니가 우리 집을 배우고 있어요.");
  render();

  let tick=0;
  const total=mappingSteps.length*4;
  const timer=setInterval(()=>{
    tick+=1;
    const ratio=Math.min(1,tick/total);
    state.mappingProgress=Math.min(100,Math.round(ratio*100));
    state.mappingStepIndex=Math.min(mappingSteps.length-1,Math.floor((tick-1)/4));
    state.progress=state.mappingProgress;
    state.soc=Math.max(MIN_SOC_AFTER_LEARNING,Math.round((startSoc-learningUse*ratio)*10)/10);
    state.firstRunEndSoc=state.soc;
    state.temperature=Math.min(33,state.temperature+0.08);
    render();
    if(tick>=total){
      clearInterval(timer);
      state.mapping=false;
      stopVacuumSound();
      playCleaningCompleteSound();
      state.profileReady=true;
      state.predicted=false;
      state.progress=100;
      state.soc=Math.max(MIN_SOC_AFTER_LEARNING,Math.round(expectedEndSoc));
      state.firstRunEndSoc=state.soc;
      const scopeSelect=$("scopeSelect"); if(scopeSelect)scopeSelect.value='home';
      const cleanModeSelect=$("cleanModeSelect"); if(cleanModeSelect)cleanModeSelect.value=activeRun.home.mopEnabled?'mop':'dry';
      const intensitySelect=$("intensitySelect"); if(intensitySelect)intensitySelect.value='standard';
      const todayStateSelect=$("todayStateSelect"); if(todayStateSelect)todayStateSelect.value='normal';
      state.temperature=29;
      state.learnCount=(state.learnCount||0)+1;
      const eventMsg="집 구조와 바닥 상태를 기억했어요. 배터리를 무리하지 않도록 여유 잔량을 남기며 학습을 마쳤어요.";
      addEvent("1회차 학습 청소 완료",eventMsg,"집 정보 저장");
      spawnEffect("🏠",8);spawnEffect("✨",9);
      render();
      setGuide("우리 집 저장 완료! 이제 오늘 청소 조건을 고르면 홈지니가 알아서 준비해요.","done");
      setTimeout(()=>{render();checkMissionUnlock();},350);
    }
  },260);
}
function selectScenario(scope,zoneNumber=null){
  if(state.cleaning||state.charging||state.mapping){showToast("학습/청소/충전이 끝난 뒤 변경할 수 있어요.");return}
  if(!state.profileReady){
    showToast("구역 선택은 1회차 학습 후 가능해요.");
    $("speech").innerHTML="<strong style='color:#ef8c32'>우리 집 학습이 먼저예요</strong><br>1회차 학습 청소를 시작해 주세요.";
    return;
  }
  if(!state.predicted){setGuide("구역을 바꾸기 전 오늘 청소 준비를 먼저 완료해 주세요.","warning");showToast("먼저 오늘 청소 준비하기를 눌러주세요.");return}
  const scopeSelect=$('scopeSelect');
  if(scopeSelect)scopeSelect.value=scope==="home"?"home":String(zoneNumber||1);
  const choices=getPredictionChoices(scope,zoneNumber);
  const matchedScenario=findMlScenarioFromChoices(choices);
  syncScenarioToState(matchedScenario);
  render();
  const status=state.soc>=state.targetSoc?"청소 가능":"충전 필요";
  const loading=$('predictLoading');
  if(loading)loading.textContent=state.selectedLabel+" 선택 · "+status+" · 홈지니가 다시 준비했어요.";
  $("speech").innerHTML="<strong>"+state.selectedLabel+" 선택!</strong><br>이 구역에 맞춰 다시 준비했어요.";
  setModeChipText("✨ "+state.selectedLabel+" 청소 준비 완료");
  setGuide((state.soc>=state.targetSoc)?state.selectedLabel+" 청소 준비가 끝났어요. 지금 바로 출동할 수 있어요.":state.selectedLabel+" 청소 준비가 끝났어요. 잠깐 충전하고 출발하면 좋아요.", state.soc>=state.targetSoc?"done":"warning");
  showToast(state.selectedLabel+" 청소 준비를 다시 맞췄어요.");
}

function openScenarioModal(){
  const enough=state.soc>=state.targetSoc;
  const title=enough?"바로 출동할 수 있어요!":"조금만 더 힘을 채울게요!";
  const scopeText=state.selectedScope==="home"?"집 전체 청소":state.selectedLabel+" 청소";
  const conditionLine="오늘 조건: <b>"+state.cleanModeLabel+" · "+state.intensityLabel+" · "+state.todayStateLabel+"</b><br><br>";
  const zoneLine=state.selectedScope==="zone"
    ? state.selectedLabel+"은 <b>"+(state.floorType||"바닥 정보")+"</b> 바닥이고, 오늘은 <b>"+(state.dirtLevel||"평소")+"</b> 상태로 준비했어요.<br><br>"
    : "저장해둔 우리 집 정보를 바탕으로 집 전체 청소를 준비했어요.<br><br>";
  const body=enough
    ? scopeText+" 준비가 끝났어요.<br><br>"+conditionLine+zoneLine+"지금 바로 시작해도 충분해요.<br>제가 배터리를 아끼면서 청소할게요!"
    : scopeText+" 준비가 끝났어요.<br><br>"+conditionLine+zoneLine+"지금 바로 출발하기엔 힘이 조금 부족해요.<br><br><b>잠깐 충전하고 나면</b><br>더 편하게 청소를 마칠 수 있어요.";
  if(enough){
    openModal(title,body);
  }else{
    openModal(title,body,{showCancel:true,cancelText:"취소",confirmText:"충전하고 시작",onConfirm:()=>chargeRobot(false)});
  }
}


function getHomeSizeType(areaPyung){
  const zoneCount=(activeRun && Number(activeRun.zoneCount)) || (activeRun && activeRun.home && Number(activeRun.home.zoneCount)) || 0;
  if(zoneCount===4)return "small";
  if(zoneCount===6)return "medium";
  if(zoneCount===8)return "large";
  const area=Number(areaPyung||0);
  if(area<=24)return "small";
  if(area<=49)return "medium";
  return "large";
}
function getHomeSizeLabel(areaPyung){
  const type=getHomeSizeType(areaPyung);
  if(type==="small")return "소형";
  if(type==="medium")return "중형";
  return "대형";
}
function getExpectedZoneCount(areaPyung){
  if(activeRun && Number(activeRun.zoneCount))return Number(activeRun.zoneCount);
  if(activeRun && activeRun.home && Number(activeRun.home.zoneCount))return Number(activeRun.home.zoneCount);
  const type=getHomeSizeType(areaPyung);
  if(type==="small")return 4;
  if(type==="medium")return 6;
  return 8;
}
function getActualZoneCount(){
  return (activeRun && activeRun.zones && activeRun.zones.length) ? activeRun.zones.length : 0;
}
function getDisplayZoneCount(){
  const actual=getActualZoneCount();
  if(actual)return actual;
  const area=(activeRun && activeRun.areaPyung) ? activeRun.areaPyung : state.areaPyung;
  return getExpectedZoneCount(area);
}
function getZoneByNumber(zoneNo){
  const zones=(activeRun && activeRun.zones) ? activeRun.zones : [];
  return zones.find(z=>Number(z.zone)===Number(zoneNo)) || zones[zoneNo-1] || null;
}
function normalizeDirtCode(zone){
  if(!zone)return 2;
  const code=Number(zone.dirtCode || zone.dirtLevelCode || 0);
  if(Number.isFinite(code) && code>0)return code;

  const text=String(zone.dirtLevel || zone.dirt || "").toLowerCase();
  if(text.includes("매우") || text.includes("심함") || text.includes("높") || text.includes("heavy") || text.includes("high"))return 4;
  if(text.includes("중") || text.includes("보통") || text.includes("normal") || text.includes("medium"))return 2;
  if(text.includes("낮") || text.includes("깨끗") || text.includes("low") || text.includes("clean"))return 1;
  return 2;
}
function getCleanableZones(){
  const blocked=state.noGoZones || [];
  const zones=(activeRun && activeRun.zones) ? activeRun.zones : [];
  return zones.filter(z=>!blocked.includes(Number(z.zone)));
}
function getAllCleanableZoneNumbers(){
  return getCleanableZones().map(z=>Number(z.zone)).filter(n=>Number.isFinite(n));
}
function getWholeHomeZones(){
  if(activeRun && activeRun.zones && activeRun.zones.length){
    return activeRun.zones.slice().sort((a,b)=>Number(a.zone)-Number(b.zone));
  }
  return [];
}
function getWholeHomeRequiredSoc(){
  // 최종 ML 구조 기준:
  // 집 전체 필요 SOC = 소형 4개 / 중형 6개 / 대형 8개 zone의 requiredSoc 합산
  const zones=getWholeHomeZones();
  if(zones.length){
    return Math.round(zones.reduce((sum,z)=>sum+Number(z.requiredSoc||0),0)*10)/10;
  }
  if(activeRun && activeRun.home){
    return Math.round(Number(activeRun.home.requiredSoc||0)*10)/10;
  }
  return 0;
}
function getWholeHomeTargetSoc(){
  // 집 전체 청소 가능하도록 필요한 SOC + 최소 잔량 15%, 최대 90% 상한 적용
  return targetFromRequired(getWholeHomeRequiredSoc());
}
function getPlannedZoneNumbers(){
  const blocked=state.noGoZones || [];

  // AI 자동청소는 반드시 '금지구역을 제외한 전체 구역'입니다.
  // 이전에 '더러운 곳만'이나 특정 구역을 눌렀던 흔적이 cleaningZones에 남아도
  // AI 자동청소에서는 그 값을 무시합니다.
  if(state.smartCleanMode==="auto"){
    return getAllCleanableZoneNumbers();
  }

  // 더러운 곳만은 오염도가 높은 일부 구역만 선택합니다.
  if(state.smartCleanMode==="dirty" && state.selectedDirtyZones && state.selectedDirtyZones.length){
    return state.selectedDirtyZones.filter(n=>!blocked.includes(Number(n))).map(Number);
  }

  // 사용자가 특정 구역을 직접 선택한 경우
  if(state.smartCleanMode==="zone" && state.selectedScope==="zone" && state.selectedZone){
    return blocked.includes(Number(state.selectedZone)) ? [] : [Number(state.selectedZone)];
  }

  // 실제 청소 진행 중에는 시작 시 확정한 청소 구역을 사용합니다.
  if(state.cleaningZones && state.cleaningZones.length){
    return state.cleaningZones.filter(n=>!blocked.includes(Number(n))).map(Number);
  }

  return getAllCleanableZoneNumbers();
}
function getDirtyRecommendationZones(){
  const cleanable=getCleanableZones();
  if(!cleanable.length)return [];
  const sorted=cleanable.slice().sort((a,b)=>getZoneConditionScore(b.zone)-getZoneConditionScore(a.zone));
  const count=Math.min(Math.max(1,Math.ceil(sorted.length*0.35)),3);
  return sorted.slice(0,count).sort((a,b)=>Number(a.zone)-Number(b.zone)).map(z=>Number(z.zone));
}
function getCurrentRecommendation(){
  if(!state.profileReady)return {icon:"🏠",title:"먼저 우리 집을 알려주세요",sub:"1회차 학습 후 맞춤 청소를 추천해요."};
  const dirty=getDirtyRecommendationZones();
  const noGo=(state.noGoZones||[]).length;
  if(dirty.length>=2)return {icon:"🔥",title:"더러운 곳만 먼저 해볼까요?",sub:dirty.join(", ")+"번 영역을 빠르게 청소할 수 있어요."};
  if(noGo>0)return {icon:"🚫",title:"금지구역은 조용히 지나갈게요",sub:"설정한 "+noGo+"곳은 빼고 청소해요."};
  return {icon:"✨",title:"AI 자동청소가 좋아요",sub:"홈지니가 오늘 상태에 맞춰 알아서 준비해요."};
}

function getZoneConditionScore(zoneNo){
  const zone=getZoneByNumber(zoneNo);
  if(!zone){
    // CSV에 아직 해당 영역 데이터가 없을 때도 화면이 비어 보이지 않도록 부드럽게 분산
    return Number(zoneNo||1) * 0.35;
  }

  const dirt=normalizeDirtCode(zone);
  const suction=Number(zone.suctionCode || zone.suctionModeCode || 0);
  const required=Number(zone.requiredSoc || 0);
  const obstacle=Number(zone.obstacleLevelCode || 0);

  // 바닥 상태 색상은 오염도 중심으로 보되,
  // 흡입 강도/장애물/필요 배터리를 조금 섞어서 구역별 차이가 잘 보이게 합니다.
  return dirt*10 + suction*2 + obstacle*1.2 + required*0.18 + Number(zoneNo||1)*0.03;
}
function getDirtVisual(zoneNo){
  const count=getDisplayZoneCount();
  const scores=[];
  for(let i=1;i<=count;i++){
    scores.push({zone:i,score:getZoneConditionScore(i)});
  }
  scores.sort((a,b)=>a.score-b.score || a.zone-b.zone);
  const rank=Math.max(0,scores.findIndex(s=>Number(s.zone)===Number(zoneNo)));
  const ratio=(rank+1)/Math.max(scores.length,1);

  // 사용자에게는 '오염도 수치'가 아니라 같은 집 안에서 상대적으로 더 신경쓸 구역을 색으로 보여줍니다.
  // 그래서 데이터가 전부 낮음/보통에 몰려도 맵에서는 구역 차이가 한눈에 보이도록 색을 넓게 분산합니다.
  if(ratio<=0.25)return {fill:"#cfeec0", label:"깨끗"};
  if(ratio<=0.55)return {fill:"#ffe08a", label:"보통"};
  if(ratio<=0.82)return {fill:"#ffb169", label:"먼지"};
  return {fill:"#ff7d68", label:"집중"};
}
function getMapZoneClass(zoneNo){
  const n=Number(zoneNo);
  const classes=[];
  const noGo=state.noGoZones || [];
  const planned=getPlannedZoneNumbers();
  const selected=state.selectedDirtyZones || [];
  const completed=state.completedZones || [];
  const dirtyHighlightOn = state.smartCleanMode==="dirty" && state.mapMode!=="noGo";

  if(noGo.includes(n))classes.push("no-go");
  else{
    if(planned.includes(n))classes.push("planned");
    if(dirtyHighlightOn && selected.includes(n))classes.push("dirty-selected");
    if(dirtyHighlightOn && selected.length && !selected.includes(n))classes.push("dimmed");
    if(state.cleaning && Number(state.currentCleaningZone)===n)classes.push("cleaning-zone");
    if(completed.includes(n))classes.push("completed");
  }
  return classes.join(" ");
}
function routeClass(){
  // 선택 직후 지도 위에 경로선이 지나가면 오류처럼 보여서,
  // 경로선은 실제 청소가 진행될 때만 표시합니다.
  const active=Boolean(state.cleaning);
  return "map-route"+(active?" active-route":"");
}
function mapRoom(x,y,w,h,rx,zoneNo,label,dashed=false){
  const visual=getDirtVisual(zoneNo);
  const isNoGo=state.noGoZones && state.noGoZones.includes(Number(zoneNo));
  const zoneClass=getMapZoneClass(zoneNo);

  const compact = h < 42 || w < 66;
  const labelSize = compact ? 11.6 : 13.0;
  const labelY = compact ? y + h * 0.57 : y + h * 0.54;
  const badgeR = compact ? 8 : 9;
  const badgeX = x + w - badgeR - 6;
  const badgeY = y + badgeR + 6;
  const badgeFont = compact ? 7.8 : 8.8;
  const centerX=x+w/2;

  let html = "<g class='map-room-group "+zoneClass+"' data-action='mapZone' data-zone='"+zoneNo+"'>"
    +"<rect class='map-room"+(dashed?" dashed":"")+"' x='"+x+"' y='"+y+"' width='"+w+"' height='"+h+"' rx='"+rx+"' fill='"+visual.fill+"'></rect>";

  if(isNoGo){
    html += "<rect class='map-no-go-shade' x='"+x+"' y='"+y+"' width='"+w+"' height='"+h+"' rx='"+rx+"'></rect>"
      +"<line class='map-no-go-line' x1='"+(x+10)+"' y1='"+(y+10)+"' x2='"+(x+w-10)+"' y2='"+(y+h-10)+"'></line>"
      +"<line class='map-no-go-line' x1='"+(x+w-10)+"' y1='"+(y+10)+"' x2='"+(x+10)+"' y2='"+(y+h-10)+"'></line>";
  }else if(state.smartCleanMode==="dirty" && state.mapMode!=="noGo" && (state.selectedDirtyZones||[]).includes(Number(zoneNo))){
    // 더러운 곳만 모드에서는 별도 아이콘 없이 초록색 테두리만 깜빡이게 표시합니다.
  }

  html += "<circle cx='"+badgeX+"' cy='"+badgeY+"' r='"+badgeR+"' fill='rgba(255,255,255,.82)'></circle>"
    +"<text class='map-room-sub' style='font-size:"+badgeFont+"px' x='"+badgeX+"' y='"+(badgeY+0.5)+"'>"+zoneNo+"</text>"
    +"<text class='map-room-label' style='font-size:"+labelSize+"px' x='"+centerX+"' y='"+labelY+"'>"+(isNoGo?"금지":label)+"</text>";

  if(!isNoGo && (state.completedZones||[]).includes(Number(zoneNo))){
    html += "<text class='map-check' x='"+(x+12)+"' y='"+(y+13)+"'>✓</text>";
  }
  html += "</g>";

  return html;
}
// 지도 레이아웃(좌표)을 한곳에 모아, 방 그리기와 로봇 위치 계산이 같은 좌표를 쓰도록 합니다.
const MAP_LAYOUTS={
  small:{viewBox:"0 0 244 162",label:"소형 집 구조 맵",route:"M42 48 C94 48, 112 96, 176 108",
    rooms:[[18,18,112,54,12,1,"거실"],[134,18,92,54,12,2,"주방"],[18,76,130,68,12,3,"침실"],[152,76,74,68,12,4,"현관",true]]},
  medium:{viewBox:"0 0 236 174",label:"중형 집 구조 맵",route:"M48 42 C96 52, 114 94, 182 98 C170 128, 118 138, 64 146",
    rooms:[[14,14,92,50,12,1,"침실"],[110,14,112,50,12,2,"주방"],[14,68,124,58,12,3,"거실"],[142,68,80,58,12,4,"서재"],[14,130,92,32,10,5,"현관"],[110,130,112,32,10,6,"다용도"]]},
  large:{viewBox:"0 0 246 172",label:"대형 집 구조 맵",route:"M46 34 C96 44, 146 36, 202 36 C174 76, 162 98, 210 92 C166 126, 102 142, 54 140",
    rooms:[[12,12,72,44,11,1,"침실1"],[88,12,72,44,11,2,"침실2"],[164,12,70,44,11,3,"주방"],[12,60,106,58,12,4,"거실"],[122,60,58,58,12,5,"아이방"],[184,60,50,58,12,6,"현관"],[12,122,106,38,10,7,"서재"],[122,122,112,38,10,8,"다용도"]]}
};
function currentMapLayout(){
  const area=(activeRun && activeRun.areaPyung) ? activeRun.areaPyung : state.areaPyung;
  return MAP_LAYOUTS[getHomeSizeType(area)]||MAP_LAYOUTS.large;
}
function getZoneRect(zoneNo){
  const r=currentMapLayout().rooms.find(x=>Number(x[5])===Number(zoneNo));
  return r?{x:r[0],y:r[1],w:r[2],h:r[3]}:null;
}
// 방 안을 지그재그(잔디깎기)로 훑는 경로 꼭짓점들
function zonePathPoints(rect){
  const m=11;
  const x0=rect.x+m,x1=rect.x+rect.w-m,y0=rect.y+m,y1=rect.y+rect.h-m;
  const rows=Math.max(2,Math.round((y1-y0)/11)+1);
  const pts=[];
  for(let r=0;r<rows;r++){
    const y=y0+(y1-y0)*r/(rows-1);
    const ltr=r%2===0;
    pts.push([ltr?x0:x1,y]);pts.push([ltr?x1:x0,y]);
  }
  return pts;
}
function pointAlong(pts,t){
  const segs=[];let total=0;
  for(let i=1;i<pts.length;i++){const d=Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]);segs.push(d);total+=d;}
  let target=clamp(t,0,1)*total;
  for(let i=0;i<segs.length;i++){
    if(target<=segs[i]||i===segs.length-1){
      const k=segs[i]?Math.min(1,target/segs[i]):1;
      return {x:pts[i][0]+(pts[i+1][0]-pts[i][0])*k,y:pts[i][1]+(pts[i+1][1]-pts[i][1])*k,dir:Math.sign(pts[i+1][0]-pts[i][0])||1,idx:i};
    }
    target-=segs[i];
  }
  return {x:pts[0][0],y:pts[0][1],dir:1,idx:0};
}
// 화면 진행률(state.progress)은 320ms 단위로 끊겨서, 로봇 아이콘은 시간 기반의 연속 진행률로 움직입니다.
function getContinuousCleanProgress(){
  const a=state.cleanAnim;
  if(!a)return Number(state.progress||0);
  const e=clamp((Date.now()-a.startedAt)/a.duration,0,1);
  return Math.min(a.fromProgress+(a.toProgress-a.fromProgress)*e,99.9);
}
function getMapRobotPose(){
  if(!state.cleaning)return null;
  const zones=(state.cleaningZones&&state.cleaningZones.length)?state.cleaningZones:getCleaningZonesForCurrentPlan();
  if(!zones.length)return null;
  const p=getContinuousCleanProgress()/100*zones.length;
  const idx=Math.min(zones.length-1,Math.floor(p));
  const sub=p-idx;
  const rect=getZoneRect(zones[idx]);
  if(!rect)return null;
  const pts=zonePathPoints(rect);
  const TRAVEL=0.16;
  if(idx>0 && sub<TRAVEL){
    const prevRect=getZoneRect(zones[idx-1]);
    const prevPts=prevRect?zonePathPoints(prevRect):pts;
    const from=prevPts[prevPts.length-1],to=pts[0];
    const k=sub/TRAVEL;
    return {x:from[0]+(to[0]-from[0])*k,y:from[1]+(to[1]-from[1])*k,dir:Math.sign(to[0]-from[0])||1,sweep:"",zone:zones[idx],idx:idx};
  }
  const t=idx>0?(sub-TRAVEL)/(1-TRAVEL):sub;
  const pos=pointAlong(pts,t);
  const swept=pts.slice(0,pos.idx+1).concat([[pos.x,pos.y]]);
  const d="M"+swept.map(q=>q[0].toFixed(1)+" "+q[1].toFixed(1)).join(" L");
  return {x:pos.x,y:pos.y,dir:pos.dir,sweep:d,zone:zones[idx],idx:idx};
}
function robotTransform(pose){
  return "translate("+pose.x.toFixed(1)+" "+pose.y.toFixed(1)+") scale("+(pose.dir<0?-1:1)+" 1)";
}
function getMapRobotMarkup(){
  const pose=getMapRobotPose();
  if(!pose)return "";
  return "<path id='mapSweep' class='map-sweep' d='"+pose.sweep+"'></path>"
    +"<g id='mapRobot' class='map-robot' transform='"+robotTransform(pose)+"'>"
    +"<circle class='map-robot-puff' cx='-9' cy='3' r='2'></circle><circle class='map-robot-puff p2' cx='-10' cy='0' r='1.6'></circle><circle class='map-robot-puff p3' cx='-8' cy='-3' r='1.3'></circle>"
    +"<ellipse class='map-robot-shadow' cx='0' cy='7.5' rx='8' ry='2.4'></ellipse>"
    +"<g class='map-robot-body'>"
    +"<circle r='8.5' class='map-robot-shell'></circle>"
    +"<rect x='-5.5' y='-0.5' width='11' height='5.5' rx='2.6' class='map-robot-face'></rect>"
    +"<circle cx='-2.6' cy='2.2' r='1' class='map-robot-eye'></circle><circle cx='2.6' cy='2.2' r='1' class='map-robot-eye'></circle>"
    +"<circle cx='0' cy='-4.6' r='1.5' class='map-robot-light'></circle>"
    +"<text class='map-robot-crown' x='0' y='-9'>👑</text>"
    +"</g></g>";
}
let mapRobotRaf=null;
function tickMapRobot(){
  mapRobotRaf=null;
  if(!state.cleaning)return;
  const pose=getMapRobotPose();
  if(pose){
    const g=$("mapRobot"),sw=$("mapSweep");
    if(g)g.setAttribute("transform",robotTransform(pose));
    if(sw)sw.setAttribute("d",pose.sweep);
    // 로봇이 다음 방으로 넘어간 순간 방 강조(초록 깜빡임/✓)도 같이 갱신
    if(Number(state.currentCleaningZone)!==Number(pose.zone)){
      const zones=(state.cleaningZones&&state.cleaningZones.length)?state.cleaningZones:getCleaningZonesForCurrentPlan();
      state.currentCleaningZone=pose.zone;
      state.completedZones=zones.slice(0,pose.idx);
      render();
    }
  }
  mapRobotRaf=requestAnimationFrame(tickMapRobot);
}
function startMapRobotAnim(){
  if(mapRobotRaf)cancelAnimationFrame(mapRobotRaf);
  mapRobotRaf=requestAnimationFrame(tickMapRobot);
}
function getMapSvg(type){
  const lay=MAP_LAYOUTS[type]||MAP_LAYOUTS.large;
  let rooms="";
  lay.rooms.forEach(r=>{rooms+=mapRoom(r[0],r[1],r[2],r[3],r[4],r[5],r[6],Boolean(r[7]));});
  return "<svg class='home-map-svg' viewBox='"+lay.viewBox+"' role='img' aria-label='"+lay.label+"'>"
    +"<path class='"+routeClass()+"' d='"+lay.route+"'></path>"
    +rooms
    +getMapRobotMarkup()
    +"</svg>";
}
function getDirtLegendHtml(){
  return "<div class='map-legend' aria-label='바닥 상태 색상 안내'>"
    +"<span class='map-legend-title'>바닥 상태</span>"
    +"<span class='map-legend-item'><i class='map-dot dot-clean'></i>깨끗</span>"
    +"<span class='map-legend-item'><i class='map-dot dot-normal'></i>보통</span>"
    +"<span class='map-legend-item'><i class='map-dot dot-dusty'></i>먼지</span>"
    +"<span class='map-legend-item'><i class='map-dot dot-focus'></i>집중</span>"
    +"</div>";
}
function getMapActionHtml(){
  const noGoCount=(state.noGoZones||[]).length;
  const noGoText=noGoCount>0 ? "금지 "+noGoCount : "금지구역";
  let hint="원하는 방식을 고른 뒤 청소하기를 누르면 돼요.";
  let readyClass=state.predicted?" status-ready":"";
  if(state.mapMode==="noGo")hint="지도에서 <b>청소하지 않을 영역</b>을 눌러주세요.";
  else if(noGoCount>0)hint="금지구역 "+noGoCount+"곳은 빼고 준비해요.";
  else if(state.smartCleanMode==="dirty")hint="초록 테두리 영역만 골라뒀어요. 청소하기를 누르면 그곳만 청소해요.";
  else if(state.smartCleanMode==="auto")hint="전체 영역을 모두 준비했어요. 금지구역만 빼고 청소해요.";

  let cleanNowLabel="🧹 바로 청소하기";
  let cleanNowSub="선택한 방식으로 바로 시작해요";
  let cleanNowDisabled="";
  if(state.cleaning){
    cleanNowLabel="🧹 청소 중이에요";
    cleanNowSub="현재 청소가 끝날 때까지 기다려 주세요";
    cleanNowDisabled=" disabled";
  }else if(state.charging){
    cleanNowLabel="🔋 충전 후 자동 출발";
    cleanNowSub="필요한 만큼 충전되면 바로 시작해요";
    cleanNowDisabled=" disabled";
  }else if(state.mapMode==="noGo"){
    cleanNowLabel="🧹 금지구역 빼고 바로 청소하기";
    cleanNowSub="선택한 금지구역을 제외하고 AI가 청소해요";
  }else if(state.smartCleanMode==="dirty"){
    cleanNowLabel="🧹 더러운 곳 바로 청소하기";
    cleanNowSub="표시된 더러운 영역만 바로 시작해요";
  }else if(state.smartCleanMode==="zone" && state.selectedZone){
    cleanNowLabel="🧹 "+state.selectedZone+"번 영역 바로 청소하기";
    cleanNowSub="선택한 영역만 바로 시작해요";
  }else{
    cleanNowSub=(state.noGoZones&&state.noGoZones.length)
      ? "금지구역 "+state.noGoZones.length+"곳을 제외하고 바로 시작해요"
      : "AI 자동청소로 바로 시작해요";
  }

  return "<div class='map-action-row'>"
    +"<button class='map-action-btn"+(state.smartCleanMode==="auto" && state.mapMode!=="noGo"?" active":"")+"' data-action='aiAutoClean'>✨ AI 자동청소</button>"
    +"<button class='map-action-btn"+(state.smartCleanMode==="dirty" && state.mapMode!=="noGo"?" active":"")+"' data-action='dirtyOnlyClean'>🔥 더러운 곳만</button>"
    +"<button class='map-action-btn danger"+(state.mapMode==="noGo"?" active":"")+"' data-action='toggleNoGoMode'>🚫 "+noGoText+"</button>"
    +"</div>"
    +"<button type='button' class='map-clean-now-btn' data-action='executeTopClean'"+cleanNowDisabled+">"
    +cleanNowLabel+"<span class='map-clean-sub'>"+cleanNowSub+"</span></button>"
    +"<div class='map-action-hint"+readyClass+"'>"+hint+"</div>";
}
function getMapRecommendationHtml(){
  if(state.predicted || state.cleaning || state.charging)return "";
  const rec=getCurrentRecommendation();
  return "<div class='map-recommend-card'><span class='rec-icon'>"+rec.icon+"</span><div><b>"+rec.title+"</b><br>"+rec.sub+"</div></div>";
}
function getMapPrepCardHtml(){
  if(!state.predicted)return "";
  const planned=getPlannedZoneNumbers();
  const noGo=(state.noGoZones||[]).length;
  let title=state.selectedLabel+" 준비 완료";
  if(state.smartCleanMode==="dirty")title="더러운 곳만 준비 완료";
  if(state.smartCleanMode==="auto")title="AI 자동청소 준비 완료";
  const sub=(noGo>0?"금지구역 "+noGo+"곳 제외 · ":"")+(planned.length?planned.length+"개 영역 청소":"청소 영역 준비")+" · "+(state.soc<state.targetSoc?"충전 후 출발":"바로 출발 가능");
  const badge=state.soc<state.targetSoc?"충전 필요":"바로 가능";
  return "<div class='map-prep-card'><div><div class='map-prep-title'>"+title+"</div><div class='map-prep-sub'>"+sub+"</div></div><div class='map-prep-badge'>"+badge+"</div></div>";
}
function getLearnedMapHtml(){
  const area=(activeRun && activeRun.areaPyung) ? activeRun.areaPyung : state.areaPyung;
  const type=getHomeSizeType(area);
  // 맵 영역에는 지도와 색상 범례만 표시합니다.
  // AI 청소 선택/실행은 아래의 별도 AI 맞춤청소 카드에서 담당합니다.
  return "<div class='home-map-card map-only-card'>"
    +"<div class='home-map-img-wrap'>"+getMapSvg(type)+"</div>"
    +getDirtLegendHtml()
    +"</div>";
}

function refreshScopeSelect(){
  const scopeSelect=$('scopeSelect');
  if(!scopeSelect)return;

  const count=getDisplayZoneCount();
  const before=scopeSelect.value || "home";

  let html="<option value='home'>집 전체</option>";
  for(let i=1;i<=count;i++){
    html += "<option value='"+i+"'>"+i+"영역</option>";
  }
  scopeSelect.innerHTML=html;
  const values=Array.from(scopeSelect.options).map(o=>o.value);
  scopeSelect.value=values.includes(before)?before:"home";
}


function setBatteryStrategy(strategy){
  if(strategy!=="care" && strategy!=="ready")return;
  if(state.cleaning || state.charging || state.mapping || state.predicting){
    showToast("진행 중인 작업이 끝난 뒤 배터리 준비 모드를 바꿀 수 있어요.");
    return;
  }
  state.batteryStrategy=strategy;
  saveBatteryStrategy();
  render();
  if(!state.profileReady){
    showToast(strategy==="ready"?"청소 준비 우선 모드를 적용할게요.":"배터리 케어 우선 모드를 적용할게요.");
    return;
  }
  if(strategy==="ready"){
    state.nextHomeTargetSoc=MAX_CHARGE_SOC;
    showToast("청소 준비 우선: 청소 후 최대 충전 상한까지 여유 있게 준비해둘게요.");
  }else{
    state.nextHomeTargetSoc=getWholeHomeTargetSoc();
    showToast("배터리 케어 우선: 다음 청소에 필요한 만큼만 준비해둘게요.");
  }
}

function renderPlan(){
  if(!$('planSummary'))return;
  refreshScopeSelect();
  const conditionPanel=$('conditionPanel');
  const learnPanel=$('learnPanel');
  const predictBtn=$('predictBtn');
  const conditionTitle=$('conditionTitle');
  const learnBtn=$('learnBtn');
  const learnActions=$('learnActions');
  const cleanExecuteBtn=$('cleanExecuteBtn');
  const learnPill=$('learnPill');
  const learnStatus=$('learnStatus');
  const learnFill=$('learnFill');
  const learnSteps=$('learnSteps');
  const learnTitle=$('learnTitle');
  const learnDesc=$('learnDesc');
  const firstLearnInputs=$('firstLearnInputs');
  const predictionInputs=$('predictionInputs');
  const startCleanPrimary=$('startCleanPrimary');
  const flowGuide=$('flowGuide');
  const mapSectionContent=$('mapSectionContent');
  const mapSectionBadge=$('mapSectionBadge');
  const aiCleanSection=$('aiCleanSection');
  const aiMappedControls=$('aiMappedControls');
  const aiHomeCleanBtn=$('aiHomeCleanBtn');
  const aiDirtyCleanBtn=$('aiDirtyCleanBtn');
  const aiNoGoBtn=$('aiNoGoBtn');
  const aiCleanSelectionNote=$('aiCleanSelectionNote');
  const aiCleanNowBtn=$('aiCleanNowBtn');
  const aiCleanNowSub=$('aiCleanNowSub');
  const batteryStrategyCareBtn=$('batteryStrategyCareBtn');
  const batteryStrategyReadyBtn=$('batteryStrategyReadyBtn');
  const batteryStrategyBadge=$('batteryStrategyBadge');
  const batteryStrategyNote=$('batteryStrategyNote');
  const batteryStrategySection=$('batteryStrategySection');
  if(flowGuide){
    const guideText=guideForCurrentState();
    let tone=state.userGuideTone||"normal";
    if(state.soc<15)tone="danger";
    else if(state.charging)tone="charging";
    else if(state.predicted && state.soc<state.targetSoc)tone="warning";
    else if(state.missionDone || state.celebrating)tone="done";
    flowGuide.className="flow-guide"+(tone&&tone!=="normal"?" "+tone:"");
    flowGuide.innerHTML="<span class='guide-step'>다음 안내</span>"+guideText;
  }

  if(mapSectionContent){
    if(state.profileReady && !state.mapping){
      setHtml(mapSectionContent,getLearnedMapHtml());
      if(mapSectionBadge){
        mapSectionBadge.textContent=getHomeSizeLabel(state.areaPyung)+' · '+getDisplayZoneCount()+'개 영역';
        mapSectionBadge.className='home-section-badge ready';
      }
    }else if(state.mapping){
      setHtml(mapSectionContent,"<div class='map-empty-state learning'><span class='map-empty-icon'>🧭</span><b>우리 집 맵을 학습 중이에요</b><span>집 구조와 바닥 상태를 기록하고 있어요.<br>학습 진행 "+state.mappingProgress+"%</span></div>");
      if(mapSectionBadge){
        mapSectionBadge.textContent='학습 '+state.mappingProgress+'%';
        mapSectionBadge.className='home-section-badge learning';
      }
    }else{
      setHtml(mapSectionContent,"<div class='map-empty-state'><span class='map-empty-icon'>🏠</span><b>우리 집 맵을 준비하고 있어요</b><span>아래 맞춤 청소 준비에서 1회차 학습을 시작하면<br>방 구조와 바닥 상태가 여기에 표시돼요.</span></div>");
      if(mapSectionBadge){
        mapSectionBadge.textContent='학습 전';
        mapSectionBadge.className='home-section-badge';
      }
    }
  }

  // 매핑 완료 후에는 학습 결과 표 대신 간단한 AI 맞춤청소 UI를 표시합니다.
  const aiReady=state.profileReady && !state.mapping;
  if(aiCleanSection)aiCleanSection.classList.toggle('ai-ready',aiReady);
  if(aiMappedControls)aiMappedControls.style.display=aiReady?'block':'none';
  if(learnPanel)learnPanel.style.display=aiReady?'none':'block';

  const strategyBusy=state.cleaning || state.charging || state.mapping || state.predicting;
  if(batteryStrategyCareBtn){
    batteryStrategyCareBtn.classList.toggle('active',state.batteryStrategy==='care');
    batteryStrategyCareBtn.disabled=strategyBusy;
  }
  if(batteryStrategyReadyBtn){
    batteryStrategyReadyBtn.classList.toggle('active',state.batteryStrategy==='ready');
    batteryStrategyReadyBtn.disabled=strategyBusy;
  }
  if(batteryStrategyBadge)batteryStrategyBadge.textContent=state.batteryStrategy==='ready'?'준비 우선':'케어 우선';
  if(batteryStrategyNote){
    batteryStrategyNote.innerHTML=state.batteryStrategy==='ready'
      ? '<b>청소 준비 우선</b> · 청소 후 최대 충전 상한까지 여유 있게 준비해요.'
      : '<b>배터리 케어 우선</b> · 청소에 필요한 만큼만 충전해요.';
  }

  if(aiReady){
    const noGoCount=(state.noGoZones||[]).length;
    const busy=state.cleaning || state.charging || state.mapping || state.predicting;

    if(aiHomeCleanBtn){
      aiHomeCleanBtn.classList.toggle('active',state.smartCleanMode==='auto' && state.mapMode!=='noGo');
      aiHomeCleanBtn.disabled=busy;
    }
    if(aiDirtyCleanBtn){
      aiDirtyCleanBtn.classList.toggle('active',state.smartCleanMode==='dirty' && state.mapMode!=='noGo');
      aiDirtyCleanBtn.disabled=busy;
    }
    if(aiNoGoBtn){
      aiNoGoBtn.classList.toggle('active',state.mapMode==='noGo');
      aiNoGoBtn.disabled=busy;
      aiNoGoBtn.innerHTML=noGoCount>0 ? '<span class="ai-mode-icon">🚫</span><span>금지구역 '+noGoCount+'곳</span>' : '<span class="ai-mode-icon">🚫</span><span>금지구역설정</span>';
    }

    if(aiCleanSelectionNote){
      if(state.mapMode==='noGo'){
        aiCleanSelectionNote.innerHTML='<b>지도에서 제외할 영역을 눌러 주세요.</b>';
      }else if(state.smartCleanMode==='dirty'){
        const dirty=(state.selectedDirtyZones||[]);
        aiCleanSelectionNote.innerHTML='<b>더러운 곳만 집중 청소</b>'+(dirty.length?' · '+dirty.join(', ')+'번 영역':'');
      }else if(state.smartCleanMode==='zone' && state.selectedZone){
        aiCleanSelectionNote.innerHTML='<b>'+state.selectedZone+'번 영역만 청소</b>';
      }else{
        aiCleanSelectionNote.innerHTML='<b>집 전체 AI 청소</b>'+(noGoCount?' · 금지구역 '+noGoCount+'곳 제외':'');
      }
    }

    if(aiCleanNowBtn){
      aiCleanNowBtn.disabled=busy;
      let main='🧹 바로 청소하기';
      let sub='선택한 AI 청소 방식으로 바로 시작해요';
      if(state.cleaning){
        main='🧹 청소 중이에요';sub='현재 청소가 끝날 때까지 기다려 주세요';
      }else if(state.charging){
        main='🔋 충전 후 자동 출발';sub='필요한 만큼 충전되면 바로 시작해요';
      }else if(state.mapMode==='noGo'){
        main='🧹 금지구역 빼고 바로 청소하기';sub='선택한 금지구역을 제외하고 집 전체를 청소해요';
      }else if(state.smartCleanMode==='dirty'){
        main='🧹 더러운 곳 바로 청소하기';sub='AI가 고른 더러운 영역만 집중 청소해요';
      }else if(state.smartCleanMode==='zone' && state.selectedZone){
        main='🧹 '+state.selectedZone+'번 영역 바로 청소하기';sub='선택한 영역만 바로 시작해요';
      }else if(state.predicted && state.soc<state.targetSoc){
        main='🔋 필요한 만큼 충전하고 청소하기';sub='과충전 없이 필요한 배터리만 채우고 출발해요';
      }
      const aiCleanNowMain=aiCleanNowBtn.querySelector('.ai-clean-now-main');
      if(aiCleanNowMain)aiCleanNowMain.textContent=main;
      if(aiCleanNowSub)aiCleanNowSub.textContent=sub;
    }
  }

  if(learnSteps){
    learnSteps.classList.remove('map-ready');
    learnSteps.innerHTML=mappingSteps.map((s,i)=>{
      let cls='learn-step';
      if(state.profileReady || i<state.mappingStepIndex)cls+=' done';
      else if(state.mapping && i===state.mappingStepIndex)cls+=' active';
      return '<div class="'+cls+'">'+s.label+'</div>';
    }).join('');
  }
  if(learnFill)learnFill.style.width=(state.profileReady?100:state.mappingProgress)+'%';

  if(state.mapping){
    if(learnTitle)learnTitle.textContent="홈지니가 우리 집을 배우고 있어요";
    if(learnDesc)learnDesc.textContent="맵·바닥 상태·배터리 사용량을 차례로 기록해요.";
    if(learnPill)learnPill.textContent="학습 중";
    if(learnStatus){
      const currentStep=mappingSteps[state.mappingStepIndex]||mappingSteps[0];
      learnStatus.innerHTML=currentStep.label+" 중 · "+state.mappingProgress+"%<br><b>배터리 "+Math.round(state.firstRunStartSoc)+"% → "+Math.round(state.soc)+"%</b>";
    }
    if(learnBtn){learnBtn.textContent="홈지니가 집을 배우는 중...";learnBtn.disabled=true;}
    if(conditionPanel)conditionPanel.classList.add('locked-area');
  }else if(state.profileReady){
    if(learnTitle)learnTitle.textContent="우리 집 AI 맞춤청소를 사용할 수 있어요";
    if(learnDesc)learnDesc.textContent="매핑된 집 정보를 바탕으로 홈지니가 청소를 알아서 준비해요.";
    if(learnPill)learnPill.textContent="AI 준비 완료";
    if(learnStatus)learnStatus.innerHTML="매핑 완료 · "+getHomeSizeLabel(activeRun.areaPyung)+" 집 구조 저장";
    if(learnBtn){learnBtn.textContent="🔄 학습 다시 실행";learnBtn.disabled=false;learnBtn.classList.add('ready');}
    if(conditionPanel)conditionPanel.classList.remove('locked-area');
  }else{
    if(learnTitle)learnTitle.textContent="처음 사용할 때는 홈지니가 집을 먼저 배워요";
    if(learnDesc)learnDesc.textContent="처음 한 번만 집 구조와 바닥 상태를 배워요.";
    if(learnPill)learnPill.textContent="초기 학습";
    if(learnStatus)learnStatus.textContent="시작 버튼을 누르면 집 정보를 저장해요.";
    if(learnBtn){learnBtn.textContent="🏠 1회차 학습 청소 시작";learnBtn.disabled=false;learnBtn.classList.remove('ready');}
    if(conditionPanel)conditionPanel.classList.remove('locked-area');
  }

  if(firstLearnInputs)firstLearnInputs.style.display=state.profileReady?'none':'block';
  if(predictionInputs)predictionInputs.style.display=state.profileReady?'block':'none';
  if(learnActions){
    learnActions.classList.toggle('ready',state.profileReady && !state.mapping);
  }
  if(cleanExecuteBtn){
    const showCleanExecute=state.profileReady && !state.mapping;
    cleanExecuteBtn.style.display=showCleanExecute?'block':'none';
    cleanExecuteBtn.disabled=!showCleanExecute || state.cleaning || state.charging || state.mapping || state.predicting;

    if(state.cleaning){
      cleanExecuteBtn.textContent='🧹 청소 중...';
    }else if(state.charging){
      cleanExecuteBtn.textContent='🔋 충전 중...';
    }else if(!state.predicted){
      cleanExecuteBtn.textContent='🧹 청소하기';
    }else if(state.soc<state.targetSoc){
      cleanExecuteBtn.textContent='🔋 충전 후 청소';
    }else{
      cleanExecuteBtn.textContent='🧹 바로 청소';
    }
  }


  if(predictBtn){
    const mainBtnDisabled=!state.profileReady || state.mapping || state.predicting || state.cleaning || state.charging;
    const key=getManualSelectionKey();
    const manualReady=state.profileReady && state.predicted && state.smartCleanMode==="manual" && state.manualReady && state.manualKey===key;

    predictBtn.disabled=mainBtnDisabled;
    predictBtn.style.opacity=mainBtnDisabled?'.55':'1';
    predictBtn.classList.toggle('running',state.predicting||state.charging||state.cleaning);

    if(!state.profileReady){
      predictBtn.textContent='🤖 학습 후 사용 가능';
    }else if(state.predicting){
      predictBtn.textContent='🤖 준비 중...';
    }else if(state.charging){
      predictBtn.textContent='🔋 충전 중...';
    }else if(state.cleaning){
      predictBtn.textContent='🧹 청소 중...';
    }else if(manualReady && state.soc<state.targetSoc){
      predictBtn.textContent='🔋 선택 조건으로 충전하고 청소하기';
    }else if(manualReady){
      predictBtn.textContent='🧹 선택 조건으로 바로 청소하기';
    }else{
      predictBtn.textContent='🔥 선택 조건으로 준비하고 청소하기';
    }
  }
  if(conditionPanel){
    conditionPanel.classList.toggle('manual-mode',state.profileReady);
  }
  if(conditionTitle){
    conditionTitle.textContent='✍️ 직접 조건 청소';
  }

  document.querySelectorAll('.scope-btn').forEach(btn=>{
    btn.classList.remove('active');
    btn.disabled=!state.profileReady || !state.predicted || state.mapping;
    btn.style.opacity=(!state.profileReady || !state.predicted || state.mapping)?'.55':'1';
  });
  if(state.selectedScope==="home")$('scopeHome').classList.add('active');
  else if($('scopeZone'+state.selectedZone))$('scopeZone'+state.selectedZone).classList.add('active');

  $('planModel').textContent=state.mapping?'집 배우는 중':(!state.profileReady?'처음 학습 전':'AI 맞춤');


  if(startCleanPrimary){
    const canStart=state.profileReady && state.predicted && !state.mapping && !state.cleaning && !state.charging;
    startCleanPrimary.disabled=!canStart;
    if(state.mapping){
      startCleanPrimary.innerHTML='🏠 우리 집을 배우는 중이에요<small id="startCleanHint">학습이 끝나면 청소 미션을 시작할 수 있어요</small>';
    }else if(!state.profileReady){
      startCleanPrimary.innerHTML='🏠 1회차 학습 청소가 먼저예요<small id="startCleanHint">집 구조를 저장한 뒤 청소할 수 있어요</small>';
    }else if(!state.predicted){
      startCleanPrimary.innerHTML='🤖 오늘 청소 준비가 먼저예요<small id="startCleanHint">홈지니가 필요한 만큼 알아서 준비해요</small>';
    }else if(state.soc<state.targetSoc){
      startCleanPrimary.innerHTML='🔋 충전하고 청소하기<small id="startCleanHint">필요한 만큼만 채우고 출발해요</small>';
    }else{
      startCleanPrimary.innerHTML='🧹 청소 미션 수행하기<small id="startCleanHint">'+state.selectedLabel+' · 바로 출동 가능</small>';
    }
  }

  if(!state.profileReady){
    $('planTargetSoc').textContent='--';
    $('planSummary').innerHTML="<div class='summary-card'><div class='summary-title'>학습 대기</div><div class='summary-row'><span class='summary-key'>상태</span><span class='summary-val'>집 정보 없음</span></div><div class='summary-row'><span class='summary-key'>다음 단계</span><span class='summary-val green'>1회차 학습 시작</span></div></div>";
    $('planSocSub').textContent="학습 후 표시";
    return;
  }
  if(!state.predicted){
    $('planTargetSoc').textContent='--';
    $('planSummary').innerHTML="<div class='summary-card'><div class='summary-title'>우리 집 저장 완료</div><div class='summary-row'><span class='summary-key'>집 크기</span><span class='summary-val'>"+state.areaPyung+"평 · "+state.cleaningAreaM2+"㎡</span></div><div class='summary-row'><span class='summary-key'>학습 중 사용</span><span class='summary-val em'>"+Math.round(state.firstRunStartSoc)+"% → "+Math.round(state.soc)+"%</span></div><div class='summary-row'><span class='summary-key'>다음 단계</span><span class='summary-val green'>오늘 청소 준비하기</span></div></div>";
    $('planSocSub').textContent="준비 대기";
    return;
  }

  $('planTargetSoc').textContent=state.targetSoc;
  const scopeText=state.selectedScope==="home"?"집 전체":state.selectedLabel;
  const detail=state.selectedScope==="home"
    ? state.areaPyung+"평 프로필 · "+state.cleaningAreaM2+"㎡"
    : (state.floorType||"바닥재질")+" · 오염도 "+(state.dirtLevel||"-")+" · "+state.cleaningAreaM2+"㎡";
  const conditionDetail=state.cleanModeLabel+" · "+state.intensityLabel+" · "+state.todayStateLabel;
  $('planSummary').innerHTML="<div class='summary-card'>"
    +"<div class='summary-title'>"+scopeText+"</div>"
    +"<div class='summary-row'><span class='summary-key'>조건</span><span class='summary-val'>"+conditionDetail+"</span></div>"
    +"<div class='summary-row'><span class='summary-key'>프로필</span><span class='summary-val'>"+detail+"</span></div>"
    +"<div class='summary-row'><span class='summary-key'>청소 준비</span><span class='summary-val em'>완료</span></div>"
    +"<div class='summary-row'><span class='summary-key'>준비 방식</span><span class='summary-val green'>"+state.matchNote+"</span></div>"
    +"</div>";
  $('planSocSub').textContent="필요한 만큼만 충전";
}

function renderHome(){
  const room=$("room");room.className="room";
  if(!state.cleaning && state.robotMotion==="returning")room.classList.add("returning");
  if(!state.cleaning && state.robotMotion==="docked")room.classList.add("docked");
  if(!state.cleaning && state.robotMotion==="departing")room.classList.add("departing");
  if(state.predicted && !state.cleaning && !state.charging && !state.chargeComplete)room.classList.add("route-preview");

  if(state.chargeComplete){
    room.classList.add("celebrate");
    if(state.chargePurpose==="nextHome"){
      $("speech").innerHTML="<strong style='color:#2f8b3a'>다음 청소 준비 완료!</strong><br>필요한 만큼 채워뒀어요.";
      setModeChipText("✅ 다음 전체 청소 준비 완료");
      $("batteryFace").textContent="😊";$("spark").textContent="💖";
      $("batteryMessage").innerHTML="다음 집 전체 청소까지<br>미리 준비해뒀어요.";
      $("timeTip").textContent="다음 청소도 바로 시작할 수 있어요.";
    }else{
      $("speech").innerHTML="<strong>배불러요!</strong><br>이제 청소 가능해요!";
      setModeChipText("💖 충전 완료 · 출동 준비");
      $("batteryFace").textContent="😍";$("spark").textContent="💖";
      $("batteryMessage").innerHTML="필요한 만큼 채웠어요.<br>출동 준비 완료!";
      $("timeTip").textContent=state.selectedLabel+" 청소를 시작할 수 있어요.";
    }
  }else if(state.celebrating){
    room.classList.add("celebrate");
    $("speech").innerHTML="<strong>청소 완료!</strong><br>보상을 받았어요!";
    setModeChipText("🏆 미션 완료 · +50 코인");
    $("batteryFace").textContent="🥳";$("spark").textContent="🎉";
  }else if(state.mapping){
    room.classList.add("cleaning");
    const step=mappingSteps[state.mappingStepIndex]||mappingSteps[0];
    $("speech").innerHTML="<strong style='color:#2f8b3a'>우리 집을 배우는 중!</strong><br>"+step.label+" 중이에요.";
    setModeChipText("🏠 학습 청소 · 배터리 "+Math.round(state.firstRunStartSoc)+"% → "+Math.round(state.soc)+"%");
    $("batteryFace").textContent="🧭";$("spark").textContent="📡";
    $("batteryMessage").innerHTML="학습 청소 중입니다.<br>배터리가 실제로 소모돼요.";
    $("timeTip").textContent="학습 진행 "+state.mappingProgress+"% · 현재 배터리 "+Math.round(state.soc)+"%";
  }else if(state.predicting){
    $("speech").innerHTML="<strong style='color:#2f8b3a'>준비 중이에요!</strong><br>오늘 상태에 맞춰 준비하고 있어요.";
    setModeChipText("🤖 우리 집 기록으로 준비 중");
    $("batteryFace").textContent="🤔";$("spark").textContent="✨";
  }else if(!state.profileReady){
    $("speech").innerHTML="<strong style='color:#ef8c32'>처음 만났어요!</strong><br>1회차 청소로 우리 집을 알려주세요.";
    setModeChipText("🏠 집 구조 학습 필요");
    $("batteryFace").textContent="🙂";$("spark").textContent="✨";
    $("batteryMessage").innerHTML="아직 우리 집 정보를 몰라요.<br>학습 청소가 필요합니다.";
    $("timeTip").textContent="1회차 학습 후 청소 준비 가능";
  }else if(!state.predicted){
    $("speech").innerHTML="<strong>집을 배웠어요!</strong><br>이제 청소 준비를 맡겨주세요.";
    setModeChipText("✅ 우리 집 저장 완료");
    $("batteryFace").textContent="😊";$("spark").textContent="✨";
    $("batteryMessage").innerHTML="집 구조 학습 완료!<br>오늘 청소 준비하기를 눌러주세요.";
    $("timeTip").textContent="청소 준비 대기 중";
  }else if(state.cleaning){
    room.classList.add("cleaning");
    $("speech").innerHTML="<strong>열심히 청소 중이에요!</strong><br>진행률 "+state.progress+"%";
    setModeChipText("🧹 "+state.selectedLabel+" 청소 중 · "+state.progress+"%");
    $("batteryFace").textContent="🧹";
    $("batteryMessage").innerHTML="청소 중입니다.<br>홈지니가 청소하면서 배터리를 사용하고 있어요.";
    $("timeTip").textContent="청소 진행률 "+state.progress+"%";
    $("spark").textContent="💨";
  }else if(state.charging){
    room.classList.add("charging");
    if(state.robotMotion==="returning"){
      if(state.chargePurpose==="nextHome"){
        $("speech").innerHTML="<strong style='color:#e48627'>스테이션으로 돌아가요</strong><br>다음 청소를 미리 준비할게요.";
        setModeChipText("🏠 다음 청소 준비 중");
      }else{
        $("speech").innerHTML="<strong style='color:#e48627'>스테이션으로 가는 중!</strong><br>잠깐 힘을 채우고 올게요.";
        setModeChipText("🏠 충전 스테이션 복귀 중");
      }
    }else{
      if(state.chargePurpose==="nextHome"){
        $("speech").innerHTML=state.batteryStrategy==="ready"
          ? "<strong style='color:#e48627'>다음 청소 준비 중!</strong><br>여유 있게 미리 준비할게요."
          : "<strong style='color:#e48627'>다음 청소 준비 중!</strong><br>필요한 만큼만 미리 채울게요.";
        setModeChipText("⚡ 다음 전체 청소 준비 중");
      }else{
        $("speech").innerHTML="<strong style='color:#e48627'>잠깐 쉬는 중이에요</strong><br>필요한 만큼만 충전할게요.";
        setModeChipText("⚡ "+state.selectedLabel+" 출동 준비 중");
      }
    }
    $("batteryFace").textContent="😌";
    $("batteryMessage").innerHTML="충전 스테이션에서 쉬면서<br>필요한 만큼만 채우고 있어요.";
    $("timeTip").textContent="홈지니가 필요한 만큼만 채우고 있어요.";
    $("spark").textContent="⚡";
  }else if(state.soc<15){
    room.classList.add("low");
    $("speech").innerHTML="<strong style='color:#ef4e45'>배가 너무 고파요...</strong><br>충전이 필요해요.";
    setModeChipText("⚠️ 배터리 부족");
    $("batteryFace").textContent="🥴";
    $("batteryMessage").innerHTML="배터리가 부족해요.<br>먼저 충전해 주세요.";
    $("timeTip").textContent="충전 후 청소를 시작해 주세요.";
    $("spark").textContent="💦";
  }else{
    setModeChipText("✨ 홈지니 맞춤 준비");
    $("batteryFace").textContent=state.soc>90?"😮":"😊";
    $("spark").textContent="✨";

    if(state.soc < state.targetSoc){
      $("speech").innerHTML=
        "<strong style='color:#ef8c32'>아직 배고파요!</strong><br>"
        + "필요한 만큼만<br>충전하고 청소할게요.";
      $("batteryMessage").innerHTML=state.selectedLabel+" 청소를 위해<br>조금 더 충전이 필요해요.";
      $("timeTip").textContent="잠깐 충전하면 청소를 시작할 수 있어요.";
    }else{
      $("speech").innerHTML="<strong>배가 든든해요!</strong><br>"+state.selectedLabel+" 청소를 준비할게요!";
      $("batteryMessage").innerHTML="현재 배터리로 충분해요.<br>바로 출동할 수 있어요.";
      $("timeTip").textContent="현재 배터리로 "+state.selectedLabel+" 청소가 가능합니다.";
    }
  }
}

/* ============================================================
   PAGE 2 · 부품 케어 (부품 상태 카드 + 수명 요약 + 실시간 케어 기록)
   ============================================================ */
function totalCleanCount(){return DEMO_CLEAN_BASE+Number(state.cleanCount||0);}
function getPartStatuses(){
  const total=totalCleanCount();
  const wheels = total>=60 ? {level:"bad",text:"점검이 필요해요"} : (total>=30 ? {level:"check",text:"한번 살펴보면 좋아요"} : {level:"good",text:"평소와 비슷해요"});
  const brush  = total>=40 ? {level:"bad",text:"머리카락을 제거해 주세요"} : (total>=8 ? {level:"check",text:"한번 살펴보면 좋아요"} : {level:"good",text:"깨끗해요"});
  const filter = total>=50 ? {level:"bad",text:"교체 시기가 됐어요"} : (total>=25 ? {level:"check",text:"한번 살펴보면 좋아요"} : {level:"good",text:"괜찮아요"});
  let battery={level:"good",text:"편안해요"};
  if(state.charging)battery={level:"good",text:"쉬면서 힘을 채우고 있어요"};
  else if(state.soc<15)battery={level:"bad",text:"배가 고파요"};
  const faces={good:"🙂",check:"😐",bad:"😟"};
  return [
    {key:"wheel",icon:"🛞",name:"바퀴 상태",...wheels,face:faces[wheels.level],
      detail:"누적 청소 "+total+"회 · 바퀴 마모가 적어 평소처럼 부드럽게 달릴 수 있어요.",tip:"바퀴 틈에 낀 실이나 머리카락은 한 달에 한 번만 빼주면 충분해요."},
    {key:"brush",icon:"🧹",name:"브러시 상태",...brush,face:faces[brush.level],
      detail:"누적 청소 "+total+"회 · 브러시에 머리카락과 털이 조금 감겼을 수 있어요.",tip:"브러시를 빼서 감긴 털을 잘라내면 흡입력이 돌아오고 모터 부담도 줄어요.",coupon:true},
    {key:"filter",icon:"🧊",name:"필터 상태",...filter,face:faces[filter.level],
      detail:"누적 청소 "+total+"회 · 필터 막힘이 적어 흡입 효율이 좋아요.",tip:"필터는 2~3주마다 톡톡 털어주고, 6개월마다 교체하면 좋아요.",coupon:true},
    {key:"battery",icon:"🔋",name:"배터리 컨디션",...battery,face:faces[battery.level],
      detail:"현재 배터리 건강도 "+state.health+"% · 500 Cycle 후 80% 성능 유지 기준",tip:"주 3회 사용 시 약 3년 1개월에 해당하며, 약 3년 주기로 점검·교체를 권장해요. 사용에 불편이 없다면 더 오래 사용할 수도 있어요."}
  ];
}
function renderCare(){
  const grid=$("partsGrid");
  if(!grid)return;
  const parts=getPartStatuses();
  setHtml(grid,parts.map(p=>
    "<button type='button' class='part-card "+p.level+"' data-action='partDetail' data-part='"+p.key+"'>"
    +"<div class='part-icon'>"+p.icon+"</div>"
    +"<div class='part-info'><div class='part-name'>"+p.name+"</div><div class='part-status'>"+p.text+"</div></div>"
    +"<div class='part-face'>"+p.face+"</div></button>").join(""));

  // 배터리 케어: 검증이 필요한 수명 연장/비용 절감 예측 대신 현재 상태와 실제 케어 행동을 보여줍니다.
  const a=$("careAcceptText"); if(a)a.textContent=state.acceptCount;
  const r=$("careReserveText"); if(r)r.textContent=state.reserveGuardCount;
  const useDay=$("batteryUseDay"); if(useDay)useDay.textContent="사용 D+"+getUsageDayCount()+"일째";

  const health=clamp(Math.round(Number(state.health||0)),0,100);
  const hf=$("careHealthFill"); if(hf)hf.style.width=health+"%";
  const ht=$("careHealthText"); if(ht)ht.textContent=health+"%";
  const hs=$("careHealthState");
  if(hs){
    hs.textContent=health>=90?"매우 좋음":(health>=80?"좋음":(health>=65?"관리 필요":"점검 권장"));
  }

  const note=$("careNote");
  if(note){
    if(state.charging && state.batteryStrategy==="ready" && state.chargePurpose==="nextHome")note.textContent="청소 준비 우선 모드로 다음 청소를 위해 여유 있게 미리 충전하고 있어요.";
    else if(state.charging)note.textContent="지금 청소에 필요한 "+state.targetSoc+"%까지만 충전하고 있어요.";
    else if(state.cleaning)note.textContent="청소 중이에요. 배터리가 너무 낮아지기 전에 스스로 쉬어가요.";
    else if(state.mapping)note.textContent="학습 청소 중에도 15% 이상 잔량을 남기도록 관리하고 있어요.";
    else if(state.batteryStrategy==="ready")note.textContent="청소 준비 우선 모드로 청소 후 최대 충전 상한까지 미리 준비해요.";
    else note.textContent="필요한 만큼만 충전하고 적정 잔량을 유지하며 배터리를 관리하고 있어요.";
  }

  const weekly=ensureWeeklyBatteryHabit();
  const weeklyTotal=Number(weekly.smartCharge||0)+Number(weekly.reserveGuard||0);
  const wg=$("weeklyBatteryGrade");
  const wm=$("weeklyBatteryMessage");
  const wp=$("weeklyChargePattern");
  const wps=$("weeklyChargePatternSub");
  const wc=$("weeklyNextCoach");
  const wcs=$("weeklyNextCoachSub");
  const wf=$("weeklyBatteryFoot");

  let grade="시작해볼까요";
  if(weeklyTotal>=5)grade="아주 좋아요";
  else if(weeklyTotal>=2)grade="좋아요";
  else if(weeklyTotal>=1)grade="잘하고 있어요";
  if(wg)wg.textContent=grade;

  if(wm){
    wm.textContent=weeklyTotal>0
      ? "이번 주 사용 패턴을 바탕으로 홈지니가 다음 배터리 습관을 알려드려요."
      : "이번 주 사용을 시작하면 홈지니가 배터리 습관을 함께 살펴드려요.";
  }

  if(state.batteryStrategy==="ready"){
    if(wp)wp.textContent="여유 준비형";
    if(wps)wps.textContent="청소 전에 배터리를 미리 여유 있게 준비하고 있어요.";
    if(wc)wc.textContent="쉬는 날엔 케어 모드";
    if(wcs)wcs.textContent="청소 계획이 없는 날에는 배터리 케어 우선으로 바꿔보세요.";
  }else{
    if(wp)wp.textContent="필요량 중심";
    if(wps)wps.textContent="청소할 만큼만 준비하는 패턴을 유지하고 있어요.";
    if(wc)wc.textContent="현재 습관 유지";
    if(wcs)wcs.textContent="지금처럼 필요한 만큼 준비하는 습관을 이어가 보세요.";
  }

  if(wf){
    wf.textContent=weeklyTotal>=5
      ? "이번 주는 배터리 사용 습관이 안정적이에요. 다음 주에도 지금 패턴을 이어가 보세요."
      : (weeklyTotal>0
          ? "사용 기록이 쌓일수록 홈지니가 더 알맞은 배터리 습관을 코칭해드려요."
          : "청소와 충전 기록이 쌓이면 이번 주 패턴에 맞는 코칭이 표시돼요.");
  }
}
function openPartDetail(el){
  const key=el && el.dataset ? el.dataset.part : el;
  const p=getPartStatuses().find(x=>x.key===key);
  if(!p)return;
  const body="<div class='modal-emoji'>"+p.icon+" "+p.face+"</div><b>"+p.text+"</b><br><br>"+p.detail+"<br><br>💡 "+p.tip;
  if(p.coupon){
    openModal(p.name,body,{showCancel:true,cancelText:"닫기",confirmText:"소모품 쿠폰 보기",onConfirm:()=>{closeModal();state.rewardTab="coupons";switchPage("rewardPage");showToast("코인으로 클린 키트 쿠폰을 교환할 수 있어요.");}});
  }else{
    openModal(p.name,body);
  }
}

/* ============================================================
   PAGE 3 · 예약 청소 (출퇴근 맞춤 예약 + 테마 기간 청소)
   ============================================================ */
const dayNames=["일","월","화","수","목","금","토"];
const themeDefs=[
  {key:"chuseok",icon:"🌕",name:"추석 맞이 대청소",start:"2026-09-18",end:"2026-09-24",desc:"가족과 손님이 오기 전, 현관과 거실을 매일 한 번씩 깨끗하게 준비해요.",chips:["집 전체","건식+물걸레","매일 1회","현관·거실 집중"]},
  {key:"season",icon:"🍂",name:"환절기 먼지 케어",start:"2026-09-01",end:"2026-10-15",desc:"창문을 자주 여는 시기라 침실 먼지를 꼼꼼 모드로 관리해요.",chips:["침실 중심","꼼꼼","주 3회","필터 점검 알림"]},
  {key:"yearend",icon:"🎄",name:"연말 대청소",start:"2026-12-20",end:"2026-12-31",desc:"한 해를 마무리하며 구역별로 나눠 무리 없이 집 전체를 정리해요.",chips:["구역 나눔","물걸레","격일","배터리 분할"]},
  {key:"spring",icon:"🌸",name:"봄맞이 새단장",start:"2027-03-01",end:"2027-03-31",desc:"꽃가루와 미세먼지가 많은 봄, 현관 매트와 거실 러그를 집중 관리해요.",chips:["현관·거실","건식","주 4회","러그 집중"]},
  {key:"rainy",icon:"☔",name:"장마철 물걸레 케어",start:"2026-06-20",end:"2026-07-20",desc:"습한 바닥을 물걸레로 자주 닦아 끈적임과 냄새를 줄여요.",chips:["마루·타일","물걸레","매일 1회","건조 시간 확보"]},
  {key:"movein",icon:"🏠",name:"이사·입주 집중 청소",start:null,end:null,desc:"새집 첫 3일, 먼지가 많은 구역부터 순서대로 집중 청소해요.",chips:["3일 집중","더러운 곳 우선","하루 2회"]}
];
function parseDay(s){return s?new Date(s+"T00:00:00"):null;}
function fmtMD(s){const d=parseDay(s);return d?(d.getMonth()+1)+"월 "+d.getDate()+"일":"";}
function themeStatus(t){
  if(!t.start)return {kind:"any",label:"언제든"};
  const today=new Date();today.setHours(0,0,0,0);
  const s=parseDay(t.start), e=parseDay(t.end);
  if(today>e)return {kind:"past",label:"지난 시즌"};
  if(today<s){const dday=Math.ceil((s-today)/86400000);return {kind:"soon",label:"D-"+dday};}
  return {kind:"live",label:"진행 중"};
}
const toMin=(hhmm)=>{const [h,m]=String(hhmm||"09:00").split(":").map(Number);return h*60+(m||0);};
const fmtMin=(m)=>{m=((m%1440)+1440)%1440;return String(Math.floor(m/60)).padStart(2,"0")+":"+String(m%60).padStart(2,"0");};
function estimateCleanMinutes(){
  const req=Number(state.profileReady?(state.predicted?state.requiredSoc:activeRun.home.requiredSoc):0);
  return req>0?Math.max(15,Math.round(req*1.4)):40;
}
function commutePlan(){
  const leave=$("leaveTime")?$("leaveTime").value:"09:00";
  const ret=$("returnTime")?$("returnTime").value:"18:30";
  const mins=estimateCleanMinutes();
  let start,end;
  if(state.commuteMode==="before"){end=toMin(ret)-60;start=end-mins;}
  else{start=toMin(leave)+30;end=start+mins;}
  return {leave,ret,mins,start:fmtMin(start),end:fmtMin(end)};
}
function commuteDayText(){
  const d=(state.commuteDays||[]).slice().sort((a,b)=>a-b);
  if(d.length===7)return "매일";
  if(d.join()==="1,2,3,4,5")return "평일";
  if(d.join()==="0,6")return "주말";
  return d.map(i=>dayNames[i]).join("·");
}
function nextCommuteRun(){
  if(!state.commuteOn||!(state.commuteDays||[]).length)return null;
  const plan=commutePlan();const now=new Date();
  for(let add=0;add<8;add++){
    const d=new Date(now);d.setDate(now.getDate()+add);
    if(!state.commuteDays.includes(d.getDay()))continue;
    const [h,m]=plan.start.split(":").map(Number);
    const startAt=new Date(d);startAt.setHours(h,m,0,0);
    if(startAt<=now)continue;
    const label=add===0?"오늘":(add===1?"내일":(d.getMonth()+1)+"월 "+d.getDate()+"일("+dayNames[d.getDay()]+")");
    return {label,plan};
  }
  return null;
}
function renderSchedule(){
  const sw=$("commuteSwitch");
  if(!sw)return;
  sw.classList.toggle("on",state.commuteOn);
  const body=$("commuteBody"); if(body)body.classList.toggle("off",!state.commuteOn);
  const chips=$("dayChips");
  if(chips)setHtml(chips,dayNames.map((n,i)=>"<button type='button' class='day-chip"+(state.commuteDays.includes(i)?" on":"")+"' data-action='toggleDay' data-day='"+i+"'>"+n+"</button>").join(""));
  const after=$("commuteAfter"),before=$("commuteBefore");
  if(after)after.classList.toggle("active",state.commuteMode==="after");
  if(before)before.classList.toggle("active",state.commuteMode==="before");

  const prev=$("commutePreview");
  if(prev){
    prev.classList.toggle("off",!state.commuteOn);
    if(!state.commuteOn){prev.textContent="스위치를 켜면 출퇴근 시간에 맞춘 예약이 만들어져요.";}
    else{
      const plan=commutePlan();
      const target=state.profileReady?(state.batteryStrategy==="ready"?MAX_CHARGE_SOC:(state.predicted?state.targetSoc:activeRun.home.targetSoc)):null;
      prev.innerHTML="<b>"+commuteDayText()+"</b> "+plan.start+" 출발 → 약 <b>"+plan.mins+"분</b> 청소 후 "+plan.end+" 도킹"
        +(target?(state.batteryStrategy==="ready"?"<br>청소 준비 우선 모드로 여유 있게 미리 준비해요.":"<br>청소에 필요한 만큼만 준비하고 출발해요."):"<br>1회차 학습을 마치면 준비 배터리와 시간이 우리 집에 맞게 정해져요.")
        +"<br>퇴근("+plan.ret+") 전에는 항상 조용히 마무리해요.";
    }
  }

  const list=$("themeList");
  if(list)setHtml(list,themeDefs.map(t=>{
    const st=themeStatus(t);const on=!!state.activeThemes[t.key];
    const period=t.start?fmtMD(t.start)+" ~ "+fmtMD(t.end):"원하는 날부터 3일";
    return "<div class='theme-card"+(on?" on":"")+(st.kind==="past"?" past":"")+"'>"
      +"<div class='theme-icon'>"+t.icon+"</div>"
      +"<div class='theme-info'><div class='theme-name'>"+t.name+"<span class='theme-state "+st.kind+"'>"+st.label+"</span></div>"
      +"<div class='theme-period'>"+period+"</div><div class='theme-desc'>"+t.desc+"</div>"
      +"<div class='theme-chips'>"+t.chips.map(c=>"<span>"+c+"</span>").join("")+"</div></div>"
      +"<button type='button' class='theme-btn"+(on?" on":"")+"' data-action='toggleTheme' data-theme='"+t.key+"'>"+(on?"예약됨 ✓":"예약하기")+"</button>"
      +"</div>";
  }).join(""));

  const up=$("upcomingList");
  if(up){
    const items=[];
    const next=nextCommuteRun();
    if(next)items.push({icon:"🚶",title:next.label+" "+next.plan.start+" 출퇴근 맞춤 청소",desc:commuteDayText()+" 반복 · "+next.plan.end+" 전 도킹 완료"});
    themeDefs.forEach(t=>{
      if(!state.activeThemes[t.key])return;
      const st=themeStatus(t);
      let desc;
      if(st.kind==="live")desc="진행 중 · "+fmtMD(t.end)+"까지 · "+t.chips[2];
      else if(st.kind==="soon")desc=fmtMD(t.start)+"부터 시작 ("+st.label+") · "+t.chips[2];
      else if(st.kind==="past")desc="이번 시즌은 지났어요. 내년 같은 시기에 다시 알려드려요.";
      else desc="시작 날짜를 정하면 3일 동안 집중 청소해요.";
      items.push({icon:t.icon,title:t.name,desc});
    });
    const badge=$("upcomingBadge"); if(badge)badge.textContent=items.length+"건";
    setHtml(up,items.length?items.map(i=>"<div class='upcoming-item'><div class='upcoming-icon'>"+i.icon+"</div><div><strong>"+i.title+"</strong><span>"+i.desc+"</span></div></div>").join("")
      :"<div class='upcoming-empty'>아직 예약이 없어요. 출퇴근 예약을 켜거나 테마 청소를 예약해 보세요.</div>");
  }
}
function fillTimeSelects(){
  const leave=$("leaveTime"),ret=$("returnTime");
  if(leave&&!leave.options.length){for(let m=6*60;m<=11*60;m+=30){const o=document.createElement("option");o.value=fmtMin(m);o.textContent=fmtMin(m);leave.appendChild(o);}leave.value="09:00";}
  if(ret&&!ret.options.length){for(let m=15*60;m<=22*60;m+=30){const o=document.createElement("option");o.value=fmtMin(m);o.textContent=fmtMin(m);ret.appendChild(o);}ret.value="18:30";}
}
function toggleCommute(){
  state.commuteOn=!state.commuteOn;
  render();
  if(state.commuteOn){
    const p=commutePlan();
    addEvent("출퇴근 예약 설정",commuteDayText()+" "+p.start+" 출발, "+p.end+" 도킹으로 예약했어요. "+(state.batteryStrategy==="ready"?"청소 준비 우선 모드로 여유 있게 준비해요.":"필요한 만큼만 충전한 뒤 출발해요."),"예약");
    showToast("출퇴근 맞춤 예약을 켰어요. 집을 비운 시간에만 청소해요.");
  }else showToast("출퇴근 맞춤 예약을 껐어요.");
}
function toggleDay(el){
  const d=Number(el.dataset.day);
  const idx=state.commuteDays.indexOf(d);
  if(idx>=0)state.commuteDays.splice(idx,1);else state.commuteDays.push(d);
  render();
}
function setCommuteMode(el){state.commuteMode=el.dataset.mode||"after";render();}
function toggleTheme(el){
  const key=el.dataset.theme;const t=themeDefs.find(x=>x.key===key);if(!t)return;
  state.activeThemes[key]=!state.activeThemes[key];
  render();
  if(state.activeThemes[key]){
    const st=themeStatus(t);
    addEvent("테마 청소 예약",t.name+"을(를) 예약했어요."+(t.start?" ("+fmtMD(t.start)+" ~ "+fmtMD(t.end)+")":""),"예약");
    showToast(t.icon+" "+t.name+" 예약 완료! "+(st.kind==="live"?"오늘부터 진행해요.":st.kind==="soon"?fmtMD(t.start)+"부터 시작해요.":"시작 시기에 알려드려요."));
  }else showToast(t.name+" 예약을 취소했어요.");
}

/* ============================================================
   PAGE 4 · 이벤트 (오늘의 발견 / 미션 / 사진첩)
   ============================================================ */
const defaultLostItems=[
  {id:"l1",emoji:"🎀",title:"거실 소파 옆",desc:"작은 머리끈으로 보여요.",place:"거실",spot:"소파 옆",time:"오늘 오후 2:15",found:false},
  {id:"l2",emoji:"🔑",title:"현관 매트 근처",desc:"작은 열쇠로 보여요.",place:"현관",spot:"매트 근처",time:"오늘 오전 10:08",found:false},
  {id:"l3",emoji:"🧦",title:"침대 옆 바닥",desc:"양말 한 짝으로 보여요.",place:"침실",spot:"침대 옆",time:"어제 오후 8:42",found:false}
];
const lostImages=(mediaData&&mediaData.lostItems)||[];
const lostItems=defaultLostItems.map((it,i)=>{
  const img=lostImages[i];const o=Object.assign({},it);
  if(img){o.src=img.src;if(img.place)o.place=img.place;if(img.time)o.time=img.time;if(img.note)o.desc=img.note;if(img.title&&img.title!==img.name.replace(/\.[^.]+$/,""))o.title=img.title;}
  return o;
});
lostImages.slice(defaultLostItems.length).forEach((img,i)=>{
  lostItems.push({id:"lx"+i,emoji:"📦",src:img.src,title:img.title||"청소 중 발견",desc:img.note||"청소 중 바닥에서 발견했어요.",place:img.place||"거실",spot:"",time:img.time||"오늘",found:false});
});
const demoPhotos=[
  {emoji:"🐶",title:"홈지니가 신기한 강아지",place:"안방",time:"오늘 오전 11:05",note:"안방에서 강아지가 홈지니에게 관심을 보여서 살포시 찍어봤어요."},
  {emoji:"🐕",title:"강아지의 하루 기록",place:"침실",time:"오늘 오전",note:"홈지니가 청소하면서 반려동물의 모습을 사진첩에 남겼어요."},
  {emoji:"🐾",title:"안방에서 쉬는 중",place:"안방",time:"오늘 오후",note:"안방에서 편안히 쉬고 있는 모습을 홈지니가 살포시 담았어요.",wide:true}
];
const realPhotos=((mediaData&&mediaData.photos)||[]).map(p=>{
  const name=String(p.name||"").toLowerCase();
  if(name==="dog3_jpg" || name==="dog3.jpg" || name==="dog3_jpg.jpg" || String(p.title||"").includes("안방에서 쉬는 중")){
    p.wide=true;
  }
  return p;
});
const photos=realPhotos.length?realPhotos:demoPhotos;
const usingDemoPhotos=!realPhotos.length;

function normalizeFoundPlace(v){
  const s=String(v||"").replace(/\s+/g,"").trim();
  if(s==="안방")return "침실";
  return s;
}
function foundMapLabelSize(label,w,h){
  const len=String(label||"").length;
  let size=11.5;
  if(len>=4)size=10;
  if(len>=5)size=9.2;
  if(w<60)size=Math.min(size,9.8);
  if(h<40)size=Math.min(size,9.3);
  return size;
}
function findFoundMapRoom(place){
  const rooms=(currentMapLayout().rooms||[]).slice();
  if(!rooms.length)return null;
  const key=normalizeFoundPlace(place);
  let room=rooms.find(r=>normalizeFoundPlace(r[6])===key);
  if(room)return room;
  if(key==="침실"){
    room=rooms.find(r=>normalizeFoundPlace(r[6]).startsWith("침실"));
    if(room)return room;
  }
  room=rooms.find(r=>normalizeFoundPlace(r[6]).includes(key) || key.includes(normalizeFoundPlace(r[6])));
  return room||rooms[0];
}
function foundMapLockedHtml(){
  return "<div class='found-map-lock'>"
    +"<div class='lock-icon'>🏠</div>"
    +"<b>집을 배운 뒤 위치를 볼 수 있어요</b>"
    +"<span>1회차 학습 청소가 끝나면<br>매핑된 집 구조에 맞춰 발견 위치를 표시해요.</span>"
    +"</div>";
}
function foundMapSvg(item){
  const lay=currentMapLayout();
  const rooms=(lay.rooms||[]).slice();
  if(!rooms.length)return "<svg viewBox='0 0 200 150' role='img' aria-label='발견 위치 지도'></svg>";
  const target=findFoundMapRoom(item&&item.place);
  const px=target ? (target[0]+target[2]/2) : 100;
  const py=target ? (target[1]+Math.max(18,target[3]*0.45)) : 75;
  const vb=String(lay.viewBox||"0 0 246 172").split(/\s+/).map(Number);
  const bx=Number.isFinite(vb[0])?vb[0]:0;
  const by=Number.isFinite(vb[1])?vb[1]:0;
  const bw=Number.isFinite(vb[2])?vb[2]:246;
  const bh=Number.isFinite(vb[3])?vb[3]:172;
  let roomMarkup="";
  rooms.forEach(r=>{
    const x=r[0],y=r[1],w=r[2],h=r[3],rad=Math.min(Number(r[4]||8),10),label=String(r[6]||"영역");
    const fontSize=foundMapLabelSize(label,w,h);
    const selected=target && Number(target[5])===Number(r[5]);
    roomMarkup += "<rect class='fm-room"+(selected?" fm-room-active":"")+"' x='"+x+"' y='"+y+"' width='"+w+"' height='"+h+"' rx='"+rad+"'/>";
    roomMarkup += "<text class='fm-label' x='"+(x+w/2)+"' y='"+(y+h/2+fontSize*0.3)+"' style='font-size:"+fontSize+"px'>"+esc(label)+"</text>";
  });
  if(target){
    roomMarkup += "<rect class='fm-focus' x='"+target[0]+"' y='"+target[1]+"' width='"+target[2]+"' height='"+target[3]+"' rx='"+Math.min(Number(target[4]||8),10)+"'/>";
  }
  return "<svg viewBox='"+lay.viewBox+"' role='img' aria-label='발견 위치 지도'>"
    +"<rect x='"+(bx+2)+"' y='"+(by+2)+"' width='"+Math.max(0,bw-4)+"' height='"+Math.max(0,bh-4)+"' rx='16' fill='#f6ead0' opacity='.55'></rect>"
    +roomMarkup
    +"<g class='fm-pin'><path d='M"+px+" "+(py+14)+" C"+(px-13)+" "+(py-2)+", "+(px-13)+" "+(py-14)+", "+px+" "+(py-14)+" C"+(px+13)+" "+(py-14)+", "+(px+13)+" "+(py-2)+", "+px+" "+(py+14)+" Z' fill='#ef8c32' stroke='#fff' stroke-width='2'/>"
    +"<circle cx='"+px+"' cy='"+(py-5)+"' r='7' fill='#fff'/><text x='"+px+"' y='"+(py-1.5)+"' text-anchor='middle' style='font-size:9px'>📍</text></g></svg>";
}
function renderFound(){
  const today=lostItems[0];
  const card=$("foundTodayCard");
  if(card&&today){
    card.innerHTML="<div class='found-card-title'>🗓️ 오늘의 발견물</div>"
      +"<div class='found-photo'>"+(today.src?"<img src='"+today.src+"' alt=''>":today.emoji)+"</div>"
      +"<div class='found-name"+(today.found?" done":"")+"'>"+(today.found?"확인 완료 ✅":"작은 물건 발견")+"</div>"
      +"<div class='found-desc'>"+esc(today.desc)+"</div>"
      +"<div class='found-meta'>📍 "+esc((today.place+" "+today.spot).trim())+"<br>🕒 "+esc(today.time)+"</div>"
      +"<div class='found-btn'><button type='button' data-action='foundItem' data-id='"+today.id+"'>더 자세히 보기 ›</button></div>";
  }
  const map=$("foundMap");
  if(map&&today)map.innerHTML=state.profileReady?foundMapSvg(today):foundMapLockedHtml();
  const mapBtn=$("foundMapBigBtn");
  if(mapBtn){
    mapBtn.disabled=!state.profileReady;
    mapBtn.textContent=state.profileReady?"지도 크게 보기 ›":"학습 후 보기";
  }
  const list=$("foundList");
  if(list)list.innerHTML=lostItems.map(it=>"<div class='found-item"+(it.found?" done":"")+"' data-action='foundItem' data-id='"+it.id+"'>"
    +"<div class='found-thumb'>"+(it.src?"<img src='"+it.src+"' alt=''>":it.emoji)+"</div>"
    +"<div><strong>"+esc(it.title)+"</strong><span>"+esc(it.desc)+"</span></div>"
    +"<div class='found-right'>📍 "+esc(it.place)+"<br>🕒 "+esc(it.time)+"</div></div>").join("");
  const badge=$("foundCountBadge"); if(badge)badge.textContent="전체 "+lostItems.length+"건";
}
function openFoundItem(el){
  const id=el&&el.dataset?el.dataset.id:el;
  const it=lostItems.find(x=>x.id===id);if(!it)return;
  const visual=it.src?"<img class='modal-img' src='"+it.src+"' alt=''>":"<div class='modal-emoji'>"+it.emoji+"</div>";
  const body=visual+"<b>"+esc(it.desc)+"</b><br>📍 "+esc((it.place+" "+it.spot).trim())+"<br>🕒 "+esc(it.time)+"<br><br>"
    +(it.found?"주인을 찾아준 물건이에요 ✅":"청소 중 움직이지 않는 작은 물건을 발견해 사진으로 남겼어요. 확인하고 제자리에 두면 다음 청소가 더 편해요.");
  if(it.found){openModal(it.title,body);return;}
  openModal(it.title,body,{showCancel:true,cancelText:"닫기",confirmText:"✅ 찾았어요",onConfirm:()=>{
    it.found=true;closeModal();state.exp+=5;levelCheck();spawnEffect("🔍",7);
    addEvent("분실물 확인","'"+it.desc+"' 을(를) 확인했어요.","발견 기록");
    renderFound();render();showToast("분실물을 확인했어요! 홈지니가 기뻐해요.");
  }});
}
function openFoundMapBig(){
  const today=lostItems[0];if(!today)return;
  if(!state.profileReady){
    openModal("발견 위치 보기","먼저 1회차 학습 청소로 집 구조를 매핑해 주세요.<br><br>매핑이 끝나면 홈지니가 배운 집 구조에 맞춰 발견 위치를 표시해요.");
    return;
  }
  openModal("발견 위치","<div class='found-map' style='height:230px;margin-bottom:10px'>"+foundMapSvg(today)+"</div>📍 <b>"+esc((today.place+" "+today.spot).trim())+"</b> · "+esc(today.time)+"<br>"+esc(today.desc));
}

const missionDefs=[
  {key:"clean",icon:"🧹",name:"청소 마스터",unit:"회 청소",tiers:[{goal:10,coins:5},{goal:100,coins:20},{goal:1000,coins:100}],get:()=>totalCleanCount()},
  {key:"charge",icon:"🔋",name:"배터리 지킴이",unit:"회 맞춤 충전",tiers:[{goal:5,coins:5},{goal:30,coins:20},{goal:100,coins:60}],get:()=>state.acceptCount},
  {key:"lost",icon:"🔍",name:"탐정 홈지니",unit:"개 분실물 발견",tiers:[{goal:3,coins:5},{goal:20,coins:20},{goal:100,coins:80}],get:()=>lostItems.length},
  {key:"photo",icon:"📷",name:"반려동물 사진가",unit:"장 촬영",tiers:[{goal:3,coins:5},{goal:30,coins:20},{goal:100,coins:80}],get:()=>photos.length},
  {key:"learn",icon:"🏠",name:"우리 집 알아가기",unit:"회 학습",tiers:[{goal:1,coins:10}],get:()=>state.learnCount}
];
const medalFor=(def,i)=>def.tiers.length===1?"🏅":(["🥉","🥈","🥇"][i]||"🏅");
function claimableCount(){
  let n=0;
  missionDefs.forEach(d=>{const v=Number(d.get()||0);d.tiers.forEach((t,i)=>{if(v>=t.goal&&!state.claimedMissions[d.key+":"+i])n++;});});
  return n;
}
function renderMissions(){
  const list=$("missionList");if(!list)return;
  const claimable=claimableCount();
  const c=$("missionClaimable");if(c)c.textContent=claimable+"개";
  const dot=$("eventNavDot");if(dot)dot.style.display=claimable>0?"inline-block":"none";
  setHtml(list,missionDefs.map(d=>{
    const v=Number(d.get()||0);
    const rows=d.tiers.map((t,i)=>{
      const key=d.key+":"+i,reached=v>=t.goal,claimed=!!state.claimedMissions[key];
      const pct=Math.min(100,Math.round(v/t.goal*100));
      let btn;
      if(claimed)btn="<button type='button' class='tier-btn claimed' disabled>받음 ✓</button>";
      else if(reached)btn="<button type='button' class='tier-btn claim' data-action='claimMission' data-key='"+key+"'>+"+t.coins+" 코인 받기</button>";
      else btn="<button type='button' class='tier-btn' disabled>+"+t.coins+" 코인</button>";
      return "<div class='tier-row"+(reached?" reached":"")+"'><div class='tier-medal'>"+medalFor(d,i)+"</div>"
        +"<div class='tier-info'><div class='tier-goal'>"+t.goal.toLocaleString()+d.unit+"</div><div class='tier-track'><div class='tier-fill' style='width:"+pct+"%'></div></div></div>"+btn+"</div>";
    }).join("");
    return "<div class='mission-card'><div class='mission-head'><span class='m-icon'>"+d.icon+"</span><span class='m-name'>"+d.name+"</span><span class='m-count'>현재 "+v.toLocaleString()+d.unit+"</span></div>"+rows+"</div>";
  }).join(""));
}
function claimMission(el){
  const key=el.dataset.key||"";const parts=key.split(":");
  const d=missionDefs.find(x=>x.key===parts[0]);if(!d)return;
  const ti=Number(parts[1]);const t=d.tiers[ti];
  if(!t||state.claimedMissions[key])return;
  if(Number(d.get()||0)<t.goal){showToast("아직 목표에 도달하지 않았어요.");return}
  state.claimedMissions[key]=true;
  state.coins+=t.coins;state.exp+=10;levelCheck();
  const medal=medalFor(d,ti);
  spawnEffect(medal,10);render();
  addEvent("도전과제 달성",d.name+" · "+t.goal.toLocaleString()+d.unit+" 메달을 받았어요. +"+t.coins+" 코인","미션");
  showToast(medal+" "+d.name+" 메달 획득! +"+t.coins+" 코인");
}
function checkMissionUnlock(){
  const n=claimableCount();
  if(n>state.notifiedClaimable){spawnEffect("🏅",6);showToast("🏅 미션 달성! 이벤트 탭에서 메달과 코인을 받아요.");}
  state.notifiedClaimable=n;
}
function renderPhotos(){
  const grid=$("photoGrid"),empty=$("photoEmpty"),count=$("photoCount");
  if(!grid)return;
  if(count)count.textContent=photos.length;
  if(empty)empty.style.display=usingDemoPhotos?"block":"none";
  grid.innerHTML=photos.map((p,i)=>"<div class='photo-tile"+(p.wide?" wide":"")+"' data-action='photoOpen' data-idx='"+i+"'>"
    +(p.src?"<img src='"+p.src+"' alt='' loading='lazy'>":"<div class='ph-emoji'>"+(p.emoji||"🐾")+"</div>")
    +"<div class='photo-cap'>"+esc(p.title)+"<small>"+esc([p.place,p.time].filter(Boolean).join(" · "))+"</small></div></div>").join("");
}
function openPhoto(el){
  const p=photos[Number(el.dataset.idx)];if(!p)return;
  const visual=p.src?"<img class='modal-img' src='"+p.src+"' alt=''>":"<div class='modal-emoji'>"+(p.emoji||"🐾")+"</div>";
  openModal(p.title||"홈지니 사진",visual+(p.place?"📍 <b>"+esc(p.place)+"</b>":"")+(p.time?" · 🕒 "+esc(p.time):"")+(p.note?"<br>"+esc(p.note):"")+"<br><br>움직임을 감지했을 때 홈지니가 자동으로 찍어둔 사진이에요.");
}
function renderEvents(){
  const tabs={found:"evTabFound",mission:"evTabMission",photo:"evTabPhoto"};
  const panels={found:"evFoundPanel",mission:"evMissionPanel",photo:"evPhotoPanel"};
  Object.keys(tabs).forEach(k=>{const b=$(tabs[k]);if(b)b.classList.toggle("active",state.eventTab===k);const p=$(panels[k]);if(p)p.classList.toggle("hidden",state.eventTab!==k);});

  // 중요: 1회차 학습이 끝나 state.profileReady가 true가 된 직후에도
  // '오늘의 발견' 지도와 사진첩을 즉시 다시 그려야 합니다.
  // 기존에는 최초 로딩 때만 renderFound()가 실행되어,
  // 학습 완료 후에도 '학습 후 보기' 잠금 화면이 그대로 남아 있었습니다.
  renderFound();
  renderPhotos();
  renderMissions();
}
function switchEventTab(tab){state.eventTab=tab;render();}

/* ============================================================
   원본 유지: 리워드 / 장식 / 모달 / 토스트 / 청소·충전 로직
   (새 페이지 연동을 위한 최소 훅만 추가: addEvent 태그, 카운터 증가)
   ============================================================ */
function renderAccessories(){
  const robot=$("robot");
  const head=$("robotHeadDeco");
  const aura=$("robotAuraDeco");
  const decal=$("robotBodyDeco");
  if(!robot || !head || !aura)return;

  robot.classList.toggle("has-custom-head",state.equippedItems.head && state.equippedItems.head!=="crown");

  const headItem=state.equippedItems.head;
  head.className="robot-accessory robot-head-deco";
  head.innerHTML="";
  if(headItem && headItem!=="crown"){
    if(headItem==="bunny"){
      head.classList.add("show","ears","bunny");
      head.innerHTML='<span class="robo-ear left"></span><span class="robo-ear right"></span>';
    }else if(headItem==="cat"){
      head.classList.add("show","ears","cat");
      head.innerHTML='<span class="robo-ear left"></span><span class="robo-ear right"></span>';
    }else if(headItem==="santa"){
      head.classList.add("show","santa");
      head.innerHTML='<span class="santa-cap"></span><span class="santa-brim"></span>';
    }else{
      const headMap={ribbon:"🎀",hat:"🧢"};
      head.textContent=headMap[headItem]||"";
      head.classList.add("show",headItem);
    }
  }

  aura.className="robot-aura-deco";
  if(state.equippedItems.aura==="sparkle"){
    aura.innerHTML="<span>✨</span><span>✨</span><span>✨</span><span>✨</span>";
    aura.classList.add("show");
  }else{
    aura.innerHTML="";
  }

  // 이전 버전 호환용: 더 이상 몸통 스티커를 사용하지 않으므로 화면에서 숨깁니다.
  if(decal){
    decal.className="robot-accessory robot-body-deco";
    decal.textContent="";
  }
}

function renderReward(){
  // 리워드 페이지에서는 레벨/경험치 패널을 표시하지 않습니다.
  // 레벨 데이터 자체는 기존 미션/성장 로직에서 그대로 유지됩니다.
  const levelText=$("levelText"); if(levelText)levelText.textContent=state.level;
  const expText=$("expText"); if(expText)expText.textContent=state.exp;
  const expFill=$("expFill"); if(expFill)expFill.style.width=state.exp+"%";

  const preview=$("levelRobotPreview");
  if(preview){
    const head=state.equippedItems.head;
    let html=''
      +'<div class="preview-shell">'
      +(head && head!=="crown" ? '' : '<span class="preview-crown">👑</span>')
      +'<div class="preview-robot">'
      +'<div class="preview-robot-top"></div>'
      +'<div class="preview-robot-face">'
      +'<div class="preview-eye left"></div>'
      +'<div class="preview-eye right"></div>'
      +'<div class="preview-cheek left"></div>'
      +'<div class="preview-cheek right"></div>'
      +'<div class="preview-mouth"></div>'
      +'</div>'
      +'<div class="preview-slot"></div>'
      +'</div>';
    if(head && head!=="crown"){
      if(head==="bunny" || head==="cat"){
        html+='<span class="preview-head ears '+head+'"><span class="p-ear left"></span><span class="p-ear right"></span></span>';
      }else if(head==="santa"){
        html+='<span class="preview-head santa"><span class="ps-cap"></span><span class="ps-brim"></span></span>';
      }else{
        const headMap={ribbon:"🎀",hat:"🧢"};
        html+='<span class="preview-head '+head+'">'+(headMap[head]||'')+'</span>';
      }
    }
    if(state.equippedItems.aura==="sparkle")html+='<span class="preview-aura"><span class="a1">✨</span><span class="a2">✨</span><span class="a3">✨</span></span>';
    html+='</div>';
    preview.innerHTML=html;
  }

  const itemTab=$("rewardTabItems");
  const couponTab=$("rewardTabCoupons");
  const itemPanel=$("rewardItemsPanel");
  const couponPanel=$("rewardCouponsPanel");
  if(itemTab)itemTab.classList.toggle("active",state.rewardTab==="items");
  if(couponTab)couponTab.classList.toggle("active",state.rewardTab==="coupons");
  if(itemPanel)itemPanel.classList.toggle("hidden",state.rewardTab!=="items");
  if(couponPanel)couponPanel.classList.toggle("hidden",state.rewardTab!=="coupons");

  updateRewardButton("santa","Santa");
  updateRewardButton("ribbon","Ribbon");
  updateRewardButton("hat","Hat");
  updateRewardButton("bunny","Bunny");
  updateRewardButton("cat","Cat");
  updateRewardButton("sparkle","Sparkle");
  updateCouponButton("lg5","CouponLg5");
  updateCouponButton("cleanKit","CouponCleanKit");
  updateCouponButton("batteryCare","CouponBatteryCare");
  updateCouponButton("moveIn","CouponMoveIn");

}

function updateRewardButton(key,suffix){
  const item=shopItems[key];
  const btn=$("btn"+suffix);
  const card=$("card"+suffix);
  const status=$("status"+suffix);
  if(!item || !btn)return;
  const owned=Boolean(state.ownedItems[key]);
  const equipped=state.equippedItems[item.slot]===item.value;
  btn.classList.remove("owned","equipped","need-coins");
  if(card){card.classList.toggle("owned",owned);card.classList.toggle("equipped",equipped);}
  if(status)status.textContent=equipped?"장착 중":(owned?"보유 중":"");
  if(equipped){btn.textContent="해제하기";btn.classList.add("equipped");}
  else if(owned){btn.textContent="장착하기";btn.classList.add("owned");}
  else{
    btn.textContent=state.coins<item.cost ? item.cost+" 코인 필요" : item.cost+" 코인";
    if(state.coins<item.cost)btn.classList.add("need-coins");
  }
}

function updateCouponButton(key,suffix){
  const item=couponItems[key];
  const btn=$("btn"+suffix);
  const card=$("card"+suffix);
  const status=$("status"+suffix);
  if(!item || !btn)return;
  const count=Number(state.ownedCoupons[key]||0);
  btn.classList.remove("owned","equipped","need-coins");
  if(card)card.classList.toggle("owned",count>0);
  if(status)status.textContent=count>0?"보유 쿠폰 "+count+"장":"";
  if(state.coins<item.cost){
    btn.textContent=item.cost+" 코인 필요";
    btn.classList.add("need-coins");
  }
  else{btn.textContent=item.cost+" 코인으로 교환";}
}


function showToast(message){
  const toast=$("toast");toast.textContent=message;toast.classList.add("show");
  clearTimeout(window.toastTimer);
  window.toastTimer=setTimeout(()=>toast.classList.remove("show"),3500);
}
let modalConfirmHandler=closeModal;
function openModal(title,body,options={}){
  $("modalTitle").textContent=title;
  $("modalBody").innerHTML=body;
  const actions=$("modalActions");
  const cancelBtn=$("modalCancel");
  const confirmBtn=$("modalConfirm");
  const showCancel=Boolean(options.showCancel);
  actions.classList.toggle("single",!showCancel);
  cancelBtn.textContent=options.cancelText||"취소";
  confirmBtn.textContent=options.confirmText||"확인";
  modalConfirmHandler=typeof options.onConfirm==="function"?options.onConfirm:closeModal;
  $("modal").classList.add("show");
}
function closeModal(){$("modal").classList.remove("show")}

function spawnEffect(symbol,count=7){
  const layer=$("effectLayer");
  for(let i=0;i<count;i++){
    const p=document.createElement("span");
    p.className="effect";p.textContent=symbol;
    p.style.setProperty("--move-x",Math.round(Math.random()*160-80)+"px");
    p.style.setProperty("--rotate",Math.round(Math.random()*100-50)+"deg");
    p.style.left=(42+Math.random()*16)+"%";
    p.style.animationDelay=(Math.random()*.22)+"s";
    layer.appendChild(p);setTimeout(()=>p.remove(),1500);
  }
}
function pulseRobot(){const robot=$("robot");robot.classList.remove("tap");void robot.offsetWidth;robot.classList.add("tap");setTimeout(()=>robot.classList.remove("tap"),650)}
function levelCheck(){if(state.exp>=100){state.exp-=100;state.level+=1;spawnEffect("⭐",10);showToast("레벨 업! Lv."+state.level)}}
// 케어 기록(2번째 탭)에 실시간으로 쌓입니다. tag는 "어떻게 수명을 지켰는지" 한 줄 라벨입니다.
function addEvent(title,description,tag){
  const list=$("eventList");
  if(!list)return;
  const now=new Date();
  const hh=String(now.getHours()).padStart(2,"0"),mm=String(now.getMinutes()).padStart(2,"0");
  const row=document.createElement("div");row.className="event-item";
  row.innerHTML='<div class="event-time">'+hh+':'+mm+'</div><div class="event-content"><strong>'+esc(title)+(tag?'<span class="event-tag">'+esc(tag)+'</span>':'')+'</strong><span>'+description+'</span></div>';
  list.prepend(row);
  while(list.children.length>30)list.removeChild(list.lastChild);
}

function petRobot(){if(state.cleaning){showToast("청소가 끝난 후 홈지니를 쓰다듬어 주세요.");return}playHomeGenieTouchSound();state.heart=Math.min(100,state.heart+2);state.exp+=1;pulseRobot();spawnEffect("💖",7);levelCheck();render();showToast("홈지니의 기분이 좋아졌어요.")}
function feedRobot(){if(state.food<=0){showToast("음식이 부족해요. 리워드에서 구매해 주세요.");return}state.food-=1;state.soc+=12;state.exp+=8;pulseRobot();spawnEffect("⚡",8);levelCheck();render();showToast("배터리가 12% 회복되었습니다.")}
function playRobot(){if(state.soc<5){showToast("배터리가 부족해서 놀 수 없어요.");return}state.soc-=3;state.exp+=5;pulseRobot();spawnEffect("💖",8);levelCheck();render();showToast("홈지니의 친밀도와 경험치가 올랐어요.")}
function trainRobot(){if(state.soc<8){showToast("훈련 전에 충전이 필요해요.");return}state.soc-=6;state.health=Math.min(100,state.health+3);state.exp+=12;pulseRobot();spawnEffect("✨",8);levelCheck();render();showToast("홈지니가 훈련을 완료했습니다.")}
function takePhoto(){pulseRobot();spawnEffect("📸",5);state.eventTab="photo";switchPage("eventPage");showToast("홈지니 사진첩을 열었어요.")}
function decorateRobot(){
  switchPage("rewardPage");
  showToast("리워드에서 아이템을 사면 홈지니에게 계속 장착돼요.");
}

function openBatteryCoachInfo(action,event){
  if(event){
    event.preventDefault();
    event.stopPropagation();
  }

  const coachVisual = `
    <div class="battery-coach-copy">
      <p>홈지니는 첫 매핑 학습으로 <b>집 크기와 청소 구역</b>을 기억해요.</p>
      <p>그래서 매번 100%까지 채우지 않아도 오늘 청소에 필요한 만큼만 준비할 수 있어요.</p>
      <p>배터리를 너무 가득 채우거나 너무 낮게 쓰는 습관을 줄이면 홈지니를 더 오래 건강하게 사용할 수 있어요.</p>
    </div>
    <div class="battery-coach-visual">
      <div class="coach-speech">
        저를 더 오래 보기 위해<br>
        <b>함께 배터리 습관을</b><br>
        지켜주실 거죠?! <span class="coach-heart">♥</span>
      </div>
      <div class="coach-robo-stage" aria-hidden="true">
        <div class="coach-robo-shadow"></div>
        <span class="coach-sparkle s1">✦</span>
        <span class="coach-sparkle s2">✦</span>
        <span class="coach-sparkle s3">✦</span>
        <div class="coach-robo">
          <div class="coach-robo-top"></div>
          <div class="coach-robo-face">
            <div class="coach-eye-wink"></div>
            <div class="coach-eye-open"></div>
            <div class="coach-cheek left"></div>
            <div class="coach-cheek right"></div>
            <div class="coach-smile"></div>
          </div>
        </div>
      </div>
    </div>`;

  openModal(
    "왜 가득 충전하지 않나요?",
    coachVisual
  );
}

function openBatteryLifeInfo(action,event){
  if(event){event.preventDefault();event.stopPropagation();}
  const usageDays=getUsageDayCount();
  const body=`
    <div style="font-size:13px;line-height:1.7;color:#6c513c;word-break:keep-all;">
      <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:13px;">
        <b style="color:#4b3324;font-size:15px;">배터리 수명·점검 기준</b>
        <span style="padding:4px 8px;border-radius:999px;background:#eaf4df;color:#2f8b3a;font-size:11px;font-weight:800;white-space:nowrap;">D+${usageDays}</span>
      </div>
      홈지니를 처음 사용한 날은 <b>${formatFirstUseDate()}</b>이고, 현재 <b>사용 D+${usageDays}일째</b>예요.<br><br>
      완전 충전 후 완전 방전을 <b>1 Cycle</b>로 보며, <b>500 Cycle 사용 후에도 80% 성능 유지</b>를 수명 시험 기준으로 봐요.<br><br>
      주 3회 사용하면 1년에 약 156회이므로 500 Cycle은 <b>약 3년 1개월</b>에 해당해요.<br><br>
      그래서 <b>약 3년 주기로 배터리 상태 점검·교체를 권장</b>해요. 사용 중 특별한 불편이 없다면 3년 이상 사용할 수도 있어요.<br><br>
      <span style="font-size:11px;color:#8a6a45;">※ 실제 사용 가능 기간은 사용 빈도와 환경에 따라 달라질 수 있어요.</span>
    </div>`;
  openModal("배터리 수명 안내",body);
}

function showStatus(){
  if(!state.profileReady){
    openModal("먼저 우리 집을 배울게요","아직 홈지니가 우리 집을 잘 몰라요.<br><br>1회차 학습 청소를 시작하면 방 구조와 바닥 상태를 기억하고, 다음부터 더 똑똑하게 청소를 준비할 수 있어요.");
    return;
  }
  if(!state.predicted){
    openModal("우리 집을 기억했어요","1회차 학습 청소가 끝났어요.<br><br>이제 오늘 청소 조건을 고르고 <b>오늘 청소 준비하기</b>를 눌러 주세요.<br>홈지니가 알아서 필요한 만큼 준비할게요.");
    return;
  }
  const scopeText=state.selectedScope==="home"?"집 전체":state.selectedLabel;
  const zoneInfo=state.selectedScope==="zone"?"<br>바닥: <b>"+(state.floorType||"정보 없음")+"</b><br>상태: <b>"+(state.dirtLevel||"평소")+"</b>":"";
  const readyText=state.soc>=state.targetSoc?"지금 바로 출동할 수 있어요.":"잠깐만 충전하면 출동할 수 있어요.";
  openModal("오늘 청소 준비 완료",scopeText+" 청소를 준비했어요."+zoneInfo+"<br><br>오늘 조건: <b>"+state.cleanModeLabel+" · "+state.intensityLabel+" · "+state.todayStateLabel+"</b><br><br>"+readyText+"<br>홈지니가 배터리를 아끼면서 청소할게요.");
}

function getRemainingCleaningSoc(){
  const total=Math.max(0,Number(state.requiredSoc||0));
  let remaining=Number(state.cleaningRemainingSoc);
  if(!Number.isFinite(remaining) || remaining<=0 || state.progress>=100 || state.missionDone){
    remaining=total;
  }
  return Math.round(Math.min(Math.max(remaining,0),total)*10)/10;
}

function resetCleaningMissionPlan(){
  state.cleaningRemainingSoc=Math.max(0,Number(state.requiredSoc||0));
  state.cleaningSegmentIndex=0;
  state.splitCleaning=state.cleaningRemainingSoc>MAX_SINGLE_PASS_USE;
  state.progress=0;
  state.missionDone=false;
}

function showSplitCleaningModal(){
  state.targetSoc=MAX_CHARGE_SOC;
  state.splitCleaning=true;
  render();
  const body="청소할 양이 많아서<br>"
    +"한 번에 무리하면 홈지니가 금방 지칠 수 있어요.<br><br>"
    +"배터리를 아끼기 위해<br>"
    +"잠깐 쉬어가며 이어서 청소할게요.";
  openModal("이번 청소는 나눠서 할게요",body,{
    showCancel:true,
    cancelText:"취소",
    confirmText:state.soc<MAX_CHARGE_SOC?"충전하고 시작":"청소 시작",
    onConfirm:()=>{
      closeModal();
      if(state.soc<MAX_CHARGE_SOC){
        chargeRobot(true);
      }else{
        startCleaning();
      }
    }
  });
}

function showReserveChargeModal(autoStartAfterCharge=false){
  const remaining=getRemainingCleaningSoc();
  const needed=targetFromRequired(remaining);
  state.targetSoc=needed;
  render();
  const body=state.selectedLabel+" 청소를 바로 시작하기엔<br>홈지니의 힘이 조금 부족해요.<br><br>잠깐 충전하고 나면<br>청소를 더 편하게 마칠 수 있어요.<br><br>필요한 만큼만 채우고 바로 출발할게요!";
  openModal("먼저 힘을 채울게요",body,{
    showCancel:true,
    cancelText:"취소",
    confirmText:"충전하고 시작",
    onConfirm:()=>{
      closeModal();
      switchPage("homePage");
      chargeRobot(autoStartAfterCharge);
    }
  });
}

function showChargeChoiceModal(autoStartAfterCharge=false){
  const remaining=getRemainingCleaningSoc();
  const needed=targetFromRequired(remaining);
  state.targetSoc=needed;
  render();
  const scopeText=state.selectedScope==="zone"?state.selectedLabel+"은 <b>"+(state.floorType||"바닥 정보")+"</b> 바닥이라 조금 더 힘이 필요해요.<br><br>":"";
  const body=scopeText+"이번 청소를 끝까지 편하게 마치려면<br>홈지니가 힘을 조금 더 채우면 좋아요.<br><br>필요한 만큼만 충전하고<br>바로 청소를 시작할게요.";
  openModal("아직 배가 조금 고파요!",body,{
    showCancel:true,
    cancelText:"취소",
    confirmText:"충전하고 시작",
    onConfirm:()=>{
      closeModal();
      switchPage("homePage");
      chargeRobot(autoStartAfterCharge);
    }
  });
}


function makeAggregateScenario(zones,label,mode){
  const areaSum=zones.reduce((sum,z)=>sum+Number(z.cleaningAreaM2||0),0);
  const requiredSum=zones.reduce((sum,z)=>sum+Number(z.requiredSoc||0),0);
  const highest=zones.slice().sort((a,b)=>getZoneConditionScore(b.zone)-getZoneConditionScore(a.zone))[0] || activeRun.home;
  return {
    scope:"home",
    zone:null,
    label:label,
    globalRunId:activeRun.home.globalRunId,
    areaPyung:activeRun.home.areaPyung,
    cleaningAreaM2:Math.round(areaSum*10)/10,
    requiredSoc:Math.round(requiredSum*10)/10,
    targetSoc:targetFromRequired(requiredSum),
    modelName:activeRun.home.modelName,
    cleaningType:activeRun.home.cleaningType,
    cleaningTypeCode:activeRun.home.cleaningTypeCode,
    mopEnabled:activeRun.home.mopEnabled,
    obstacleLevel:activeRun.home.obstacleLevel,
    obstacleLevelCode:activeRun.home.obstacleLevelCode,
    floorType:highest.floorType || activeRun.home.floorType,
    dirtLevel:highest.dirtLevel || activeRun.home.dirtLevel,
    dirtCode:highest.dirtCode || activeRun.home.dirtCode,
    suctionMode:highest.suctionMode || activeRun.home.suctionMode,
    suctionCode:highest.suctionCode || activeRun.home.suctionCode,
    cleanModeChoice:state.cleanModeChoice,
    cleanModeLabel:state.cleanModeLabel,
    intensityChoice:state.intensityChoice,
    intensityLabel:state.intensityLabel,
    todayStateChoice:state.todayStateChoice,
    todayStateLabel:state.todayStateLabel,
    matchNote:mode==="dirty"?"먼지가 많은 곳만 골라 준비":"금지구역은 빼고 알아서 준비",
    matchBasis:"우리 집 매핑 정보 반영"
  };
}
function prepareScenarioAndShow(scenario,message,tone="done"){
  state.chargePurpose='current';
  state.nextHomeReady=false;
  syncScenarioToState(scenario);
  state.predicted=true;
  state.predicting=false;
  state.chargeComplete=false;
  state.cleaningRemainingSoc=Number(state.requiredSoc||0);
  state.progress=0;
  render();
  const canNow=state.soc>=state.targetSoc;
  $("speech").innerHTML="<strong style='color:#2f8b3a'>준비 완료!</strong><br>"+(canNow?"바로 출동할 수 있어요.":"잠깐 충전하고 출발할게요.");
  setModeChipText("✅ "+state.selectedLabel+" 준비 완료");
  setGuide(message,canNow?tone:"warning");
  showToast(message.replace(/<[^>]*>/g,""));
}
function aiAutoClean(){
  if(!state.profileReady){showToast("먼저 1회차 학습 청소를 시작해 주세요.");return}
  if(state.mapping||state.cleaning||state.charging){showToast("진행 중인 작업이 끝난 뒤 선택할 수 있어요.");return}

  const cleanable=getCleanableZones();
  const allZones=cleanable.map(z=>Number(z.zone));
  if(!cleanable.length){showToast("청소할 수 있는 영역이 없어요. 금지구역을 줄여주세요.");return}

  state.mapMode="view";
  state.smartCleanMode="auto";
  state.selectedScope="home";
  state.selectedZone=null;
  state.manualReady=false;
  state.manualKey="";
  state.selectedDirtyZones=[];
  state.completedZones=[];
  state.currentCleaningZone=null;
  state.cleaningZones=allZones;

  // 핵심: AI 자동청소는 항상 전체 zone SOC 합산값을 사용합니다.
  // 금지구역이 있으면 그 구역만 제외하고 합산합니다.
  const scenario=makeAggregateScenario(cleanable,"집 전체 청소","auto");
  scenario.scope="home";
  scenario.label="집 전체 청소";
  scenario.requiredSoc=Math.round(cleanable.reduce((sum,z)=>sum+Number(z.requiredSoc||0),0)*10)/10;
  scenario.targetSoc=targetFromRequired(scenario.requiredSoc);
  scenario.matchNote=(state.noGoZones&&state.noGoZones.length)
    ? "금지구역을 제외한 전체 청소"
    : "전체 구역 자동청소";
  scenario.matchBasis=allZones.length+"개 영역 모두 반영";

  prepareScenarioAndShow(
    scenario,
    "집 전체 청소 준비 완료! 매핑된 "+allZones.length+"개 영역을 모두 청소할게요.",
    "done"
  );
}
function dirtyOnlyClean(){
  if(!state.profileReady){showToast("먼저 1회차 학습 청소를 시작해 주세요.");return}
  if(state.mapping||state.cleaning||state.charging){showToast("진행 중인 작업이 끝난 뒤 선택할 수 있어요.");return}
  state.mapMode="view";
  state.smartCleanMode="dirty";
  state.manualReady=false;
  state.manualKey="";

  const cleanable=getCleanableZones();
  if(!cleanable.length){showToast("청소할 수 있는 영역이 없어요. 금지구역을 줄여주세요.");return}

  const sorted=cleanable.slice().sort((a,b)=>getZoneConditionScore(b.zone)-getZoneConditionScore(a.zone));
  const count=Math.min(Math.max(1,Math.ceil(sorted.length*0.35)),3);
  const picked=sorted.slice(0,count).sort((a,b)=>Number(a.zone)-Number(b.zone));
  state.selectedDirtyZones=picked.map(z=>Number(z.zone));
  state.cleaningZones=state.selectedDirtyZones.slice();
  state.completedZones=[];
  state.currentCleaningZone=null;

  const scenario=makeAggregateScenario(picked,"더러운 곳만","dirty");
  prepareScenarioAndShow(scenario,"더 신경 쓸 곳만 골랐어요. 이 영역부터 깨끗하게 청소할게요.","done");
}
function toggleNoGoMode(){
  if(!state.profileReady){showToast("먼저 1회차 학습 청소를 시작해 주세요.");return}
  if(state.mapping||state.cleaning||state.charging){showToast("진행 중인 작업이 끝난 뒤 설정할 수 있어요.");return}

  state.mapMode = state.mapMode==="noGo" ? "view" : "noGo";
  if(state.mapMode==="noGo"){
    state.smartCleanMode="auto";
    state.selectedDirtyZones=[];
    state.completedZones=[];
    state.currentCleaningZone=null;
    state.cleaningZones=getCleanableZones().map(z=>Number(z.zone));
    setGuide("청소하지 않을 영역을 지도에서 눌러주세요. 다시 누르면 해제돼요.","warning");
    showToast("금지구역 설정: 지도에서 제외할 영역을 눌러주세요.");
  }else{
    const count=(state.noGoZones||[]).length;
    setGuide(count>0?"금지구역 "+count+"곳을 빼고 청소할 수 있어요.":"금지구역 설정을 마쳤어요.","done");
    showToast(count>0?"금지구역 "+count+"곳을 저장했어요.":"금지구역 설정을 마쳤어요.");
  }
  render();
}
function handleMapZoneTap(element){
  const zoneNo=Number(element && element.dataset ? element.dataset.zone : element);
  if(!zoneNo)return;
  if(!state.profileReady){showToast("1회차 학습 후 지도에서 선택할 수 있어요.");return}

  if(state.mapMode==="noGo"){
    const list=state.noGoZones || [];
    const idx=list.indexOf(zoneNo);
    if(idx>=0){
      list.splice(idx,1);
      showToast(zoneNo+"번 영역 금지구역을 해제했어요.");
    }else{
      list.push(zoneNo);
      list.sort((a,b)=>a-b);
      showToast(zoneNo+"번 영역은 청소하지 않을게요.");
    }
    state.noGoZones=list;
    state.predicted=false;
    state.manualReady=false;
    state.manualKey="";
    state.smartCleanMode="auto";
    state.selectedDirtyZones=[];
    state.completedZones=[];
    state.currentCleaningZone=null;
    state.cleaningZones=getCleanableZones().map(z=>Number(z.zone));
    render();
    return;
  }

  // 일반 보기 상태의 맵은 정보 확인용으로 유지합니다.
  // 특정 영역을 세부 조건으로 청소하려면 아래 '직접조건 청소'에서 선택할 수 있습니다.
  showToast(zoneNo+"번 영역 · 세부 청소 조건은 아래 '직접조건 청소'에서 설정할 수 있어요.");
}




function manualCleanAndGo(){
  if(state.cleaning){showToast("이미 청소 중이에요.");return}
  if(state.charging){showToast("충전이 끝나면 바로 출발할게요.");return}
  if(state.mapping){showToast("집을 다 배운 뒤 청소할 수 있어요.");return}
  if(!state.profileReady){
    setGuide("먼저 1회차 학습 청소로 우리 집을 알려주세요.","warning");
    showToast("먼저 홈지니에게 우리 집을 알려주세요.");
    return;
  }

  const key=getManualSelectionKey();
  const manualReady=state.predicted && state.smartCleanMode==="manual" && state.manualReady && state.manualKey===key;

  // 조건이 아직 적용되지 않았거나 바뀌었다면:
  // 1) 선택 조건으로 청소 준비
  // 2) 준비가 끝나면 자동으로 충전/청소까지 이어짐
  if(!manualReady){
    predictSocFromConditions(true);
    return;
  }

  // 이미 같은 조건으로 준비되어 있으면 바로 충전/청소 실행
  executeTopClean();
}

function executeTopClean(){
  if(state.cleaning){showToast("이미 청소 중이에요.");return}
  if(state.charging){showToast("충전이 끝난 뒤 바로 출발할게요.");return}
  if(state.mapping){showToast("집을 다 배운 뒤 청소할 수 있어요.");return}
  if(!state.profileReady){
    setGuide("먼저 1회차 학습 청소로 우리 집을 알려주세요.","warning");
    showToast("먼저 홈지니에게 우리 집을 알려주세요.");
    return;
  }

  // 사용자가 따로 선택하지 않으면 가장 쉬운 기본값인 AI 자동청소로 준비합니다.
  if(!state.predicted){
    aiAutoClean();
    if(!state.predicted)return;
  }

  if(state.soc < state.targetSoc){
    if(Number(state.requiredSoc||0)>MAX_SINGLE_PASS_USE && state.soc<MAX_CHARGE_SOC){
      showSplitCleaningModal();
    }else{
      chargeRobot(true);
    }
  }else{
    state.robotMotion='idle';
    startCleaning();
  }
}


function getCleaningZonesForCurrentPlan(){
  if(state.smartCleanMode==="auto"){
    return getAllCleanableZoneNumbers();
  }
  const nums=getPlannedZoneNumbers();
  if(nums.length)return nums;
  if(state.selectedScope==="zone" && state.selectedZone)return [Number(state.selectedZone)];
  return getAllCleanableZoneNumbers();
}
function updateCleaningZoneProgress(percent){
  const zones=state.cleaningZones && state.cleaningZones.length ? state.cleaningZones : getCleaningZonesForCurrentPlan();
  if(!zones.length){
    state.currentCleaningZone=null;
    state.completedZones=[];
    return;
  }
  const ratio=clamp(Number(percent||0),0,99)/100;
  const idx=Math.min(zones.length-1,Math.floor(ratio*zones.length));
  state.currentCleaningZone=zones[idx];
  state.completedZones=zones.slice(0,idx);
}
function finishCleaningZoneProgress(){
  const zones=state.cleaningZones && state.cleaningZones.length ? state.cleaningZones : getCleaningZonesForCurrentPlan();
  state.completedZones=zones.slice();
  state.currentCleaningZone=null;
}
function clearCleaningZoneProgress(){
  state.cleaningZones=[];
  state.currentCleaningZone=null;
  state.completedZones=[];
}


function startCleaning(){
  if(state.cleaning){showToast("이미 청소 중이에요.");return}
  if(state.charging){showToast("충전이 끝난 후 청소할게요.");return}
  if(state.mapping){showToast("1회차 학습이 끝난 뒤 청소할 수 있어요.");return}
  if(!state.profileReady){
    setGuide("아직 홈지니가 우리 집을 잘 몰라요. 먼저 1회차 학습 청소를 시작해 주세요.","warning");
    showToast("먼저 홈지니에게 우리 집을 알려주세요.");
    $("speech").innerHTML="<strong style='color:#ef8c32'>학습이 먼저예요</strong><br>집 정보를 저장한 뒤 청소할 수 있어요.";
    switchPage("homePage");
    return;
  }
  if(!state.predicted){
    showToast("청소 전 오늘 청소 준비하기를 먼저 눌러주세요.");
    $("speech").innerHTML="<strong style='color:#2f8b3a'>청소 준비가 필요해요</strong><br>오늘 상태를 먼저 알려주세요.";
    switchPage("homePage");
    return;
  }

  const totalRequired=Math.max(0,Number(state.requiredSoc||0));
  if(totalRequired<=0){showToast("오늘 청소 준비를 다시 실행해 주세요.");return}

  if(state.missionDone || state.progress>=100){
    resetCleaningMissionPlan();
  }

  let remaining=getRemainingCleaningSoc();

  // 90% 상한과 15% 잔량 기준으로 한 번에 끝낼 수 없는 경우에만 분할 청소 안내를 띄웁니다.
  if(remaining>MAX_SINGLE_PASS_USE && state.soc<MAX_CHARGE_SOC){
    showSplitCleaningModal();
    return;
  }

  const neededStart=targetFromRequired(remaining);
  state.targetSoc=neededStart;

  // 청소 시작 전 Reserve 배터리 Guard
  if(remaining<=MAX_SINGLE_PASS_USE && state.soc<neededStart){
    showReserveChargeModal(true);
    return;
  }

  if(state.soc<=MIN_RESERVE_SOC){
    showReserveChargeModal(true);
    return;
  }

  const availableUse=Math.max(0,Number(state.soc||0)-MIN_RESERVE_SOC);
  let segmentUse=remaining;
  let segmentWillComplete=true;

  // 분할 청소 중 첫 구간: 현재 배터리에서 15%를 남길 수 있는 만큼만 청소
  if(remaining>availableUse){
    segmentUse=availableUse;
    segmentWillComplete=false;
  }

  if(segmentUse<=0){
    showReserveChargeModal(true);
    return;
  }

  state.cleaning=true;
  startVacuumSound();
  // 바로 청소 가능한 경우에는 스테이션 복귀/출발 모션 없이 즉시 청소를 시작합니다.
  // 스테이션 출발 모션은 실제 충전 후 자동 출발할 때만 chargeRobot()에서 실행합니다.
  state.robotMotion='idle';
  state.cleaningZones=getCleaningZonesForCurrentPlan();
  updateCleaningZoneProgress(state.progress||0);
  state.chargeComplete=false;
  state.missionDone=false;
  const startSoc=Number(state.soc||0);
  const startProgress=Number(state.progress||0);
  const progressGain=Math.max(1,Math.round(segmentUse/totalRequired*100));
  const endProgress=segmentWillComplete?100:Math.min(99,startProgress+progressGain);
  const endSoc=Math.max(MIN_RESERVE_SOC,Math.round((startSoc-segmentUse)*10)/10);
  state.cleaningSegmentIndex+=1;
  // 지도 위 로봇 아이콘을 부드럽게 움직이기 위한 시간 기반 진행 정보
  state.cleanAnim={startedAt:Date.now(),duration:20*320,fromProgress:startProgress,toProgress:endProgress};
  render();
  startMapRobotAnim();
  setGuide(state.selectedLabel+" 청소를 시작했어요. 홈지니가 배터리를 아끼면서 깨끗하게 청소할게요.","normal");
  showToast("청소 시작! 홈지니가 배터리를 아끼며 청소해요.");

  let step=0;
  const totalSteps=20;
  const timer=setInterval(()=>{
    step+=1;
    const ratio=step/totalSteps;
    state.progress=Math.round(startProgress+(endProgress-startProgress)*ratio);
    updateCleaningZoneProgress(state.progress);
    state.soc=Math.max(MIN_RESERVE_SOC,Math.round((startSoc-segmentUse*ratio)*10)/10);
    state.temperature=Math.min(36,state.temperature+.25);
    render();

    if(state.soc<=CRITICAL_DOCK_SOC && !segmentWillComplete){
      step=totalSteps;
    }
    if(state.cleanAnim && step>=totalSteps)state.cleanAnim.duration=Math.max(1,Date.now()-state.cleanAnim.startedAt);

    if(step>=totalSteps){
      clearInterval(timer);
      state.cleaning=false;
      stopVacuumSound();
      state.cleanAnim=null;
      state.temperature=29;
      state.soc=endSoc;
      const newRemaining=Math.max(0,Math.round((remaining-segmentUse)*10)/10);
      state.cleaningRemainingSoc=newRemaining;

      if(newRemaining>0.2){
        state.progress=endProgress;
        updateCleaningZoneProgress(state.progress);
        state.robotMotion='returning';
        state.targetSoc=targetFromRequired(newRemaining);
        // [부품케어 탭 연동] 15% 잔량 보호 횟수 + 케어 기록
        state.reserveGuardCount+=1;
        ensureWeeklyBatteryHabit().reserveGuard+=1;
        saveWeeklyBatteryHabit();
        addEvent("잠깐 쉬어가기",state.selectedLabel+" 청소 중 배터리 잔량이 낮아져 스스로 도킹했어요. 잠깐 충전 후 남은 곳을 이어서 청소해요.","저잔량 보호");
        render();
        $("speech").innerHTML="<strong style='color:#ef8c32'>잠깐 쉬어갈게요!</strong><br>조금만 쉬고 다시 힘낼게요.";
        setGuide("홈지니가 조금 지쳤어요. 잠깐 충전하고 남은 곳을 이어서 청소할게요.","warning");
        showToast("잠깐 충전하고 남은 곳을 이어서 청소할게요.");
        setTimeout(()=>openModal("잠깐 쉬어갈게요!","제가 조금 지쳤어요.<br>잠깐 충전하고 나면<br>남은 곳도 다시 힘내서 청소할게요!<br><br>지금 배터리: <b>"+fmtSoc(state.soc)+"%</b>",{
          showCancel:true,
          cancelText:"나중에",
          confirmText:"충전하고 이어서",
          onConfirm:()=>{closeModal();chargeRobot(true);}
        }),450);
        return;
      }

      playCleaningCompleteSound();
      state.cleaningRemainingSoc=0;
      state.progress=100;
      finishCleaningZoneProgress();
      state.robotMotion='idle';
      state.missionDone=true;
      state.celebrating=true;
      state.cleanCount+=1;
      state.coins+=50;
      state.exp+=20;
      state.area=Math.round((state.area||0)+(state.cleaningAreaM2||0));
      state.average=Math.round((state.average+Math.max(15,Math.round(state.requiredSoc*1.4)))/2);
      levelCheck();
      // [부품케어 탭 연동] 배터리 절약 기록
      addEvent(state.selectedLabel+" 청소 완료","배터리를 아껴 쓰며 청소를 마쳤어요. 적정 잔량을 남겨 배터리에 무리를 주지 않았어요.","배터리 보호");
      spawnEffect("🎉",15);spawnEffect("⭐",9);
      render();
      $("speech").innerHTML="<strong style='color:#2f8b3a'>청소 완료!</strong><br>+50코인을 받았어요.";
      setModeChipText("🏆 "+state.selectedLabel+" 완료 · +50코인");
      setGuide("청소 완료! 배터리를 아껴 쓰며 마무리했어요. 보상으로 +50코인과 경험치를 받았어요.","done");
      showToast("청소 완료! 홈지니가 +50코인을 가져왔어요.");
      setTimeout(()=>{
        state.celebrating=false;
        clearCleaningZoneProgress();
        render();
        // 청소가 끝나면 다음 집 전체 청소에 필요한 만큼 미리 충전합니다.
        // 소형/중형/대형별 4/6/8개 zone의 requiredSoc 합산값을 기준으로 목표 충전량을 정합니다.
        setTimeout(prepareNextWholeHomeCharge,350);
      },3600);
      // [이벤트 탭 연동] 미션 달성 알림
      setTimeout(checkMissionUnlock,4200);
    }
  },320);
}

function prepareNextWholeHomeCharge(){
  if(state.mapping || state.cleaning || state.charging)return;
  if(!state.profileReady || !activeRun)return;

  const wholeRequired=getWholeHomeRequiredSoc();
  if(wholeRequired<=0)return;

  const wholeTarget=state.batteryStrategy==="ready" ? MAX_CHARGE_SOC : getWholeHomeTargetSoc();
  const wholeZones=getWholeHomeZones();

  state.nextHomeRequiredSoc=wholeRequired;
  state.nextHomeTargetSoc=wholeTarget;
  state.targetSoc=wholeTarget;
  state.requiredSoc=wholeRequired;
  state.cleaningRemainingSoc=wholeRequired;
  state.progress=0;
  state.selectedScope="home";
  state.selectedZone=null;
  state.selectedLabel="다음 전체 청소";
  state.smartCleanMode="auto";
  state.cleaningZones=wholeZones.map(z=>Number(z.zone));
  state.selectedDirtyZones=[];
  state.completedZones=[];
  state.currentCleaningZone=null;
  state.predicted=true;
  state.chargePurpose="nextHome";

  if(state.soc>=wholeTarget){
    state.nextHomeReady=true;
    state.chargeComplete=true;
    render();
    const msg=state.batteryStrategy==="ready"
      ? "청소 준비 우선 모드로 다음 청소를 위해 여유 있게 준비해뒀어요."
      : "다음 전체 청소도 바로 할 수 있게 필요한 만큼 준비해뒀어요.";
    const speech=$("speech");
    if(speech)speech.innerHTML=state.batteryStrategy==="ready"
      ? "<strong style='color:#2f8b3a'>청소 준비 완료!</strong><br>여유 있게 미리 준비해뒀어요."
      : "<strong style='color:#2f8b3a'>다음 청소 준비 완료!</strong><br>필요한 만큼 채워뒀어요.";
    const chip=$("modeChip");
    if(chip)chip.textContent="✅ 다음 전체 청소 준비 완료";
    setGuide(msg,"done");
    showToast(msg);
    setTimeout(()=>{state.chargeComplete=false;render();},2600);
    return;
  }

  state.nextHomeReady=false;
  if(state.batteryStrategy==="ready"){
    setGuide("청소가 끝났어요. 청소 준비 우선 모드로 최대 충전 상한까지 미리 준비해둘게요.","charging");
    showToast("다음 청소에 바로 나갈 수 있게 여유 있게 준비할게요.");
  }else{
    setGuide("청소가 끝났어요. 다음 전체 청소에 필요한 만큼만 미리 충전해둘게요.","charging");
    showToast("다음 청소에 필요한 만큼만 미리 힘을 채울게요.");
  }
  chargeRobot(false,"nextHome");
}

function chargeRobot(autoStart=false,purpose='current'){
  if(state.cleaning){showToast("청소가 끝난 후 충전할 수 있어요.");return}
  if(state.charging){showToast("이미 충전 중이에요.");return}
  state.chargePurpose=purpose || 'current';
  const isNextHomeCharge=state.chargePurpose==='nextHome';
  if(state.soc>=state.targetSoc){
    if(autoStart){state.robotMotion='idle';setTimeout(startCleaning,250);return}
    state.chargeComplete=true;
    if(isNextHomeCharge)state.nextHomeReady=true;
    render();
    const speech=$("speech");
    const chip=$("modeChip");
    if(isNextHomeCharge){
      if(speech)speech.innerHTML=state.batteryStrategy==="ready"
        ? "<strong style='color:#2f8b3a'>청소 준비 완료!</strong><br>여유 있게 미리 준비해뒀어요."
        : "<strong style='color:#2f8b3a'>다음 청소 준비 완료!</strong><br>필요한 만큼 채워뒀어요.";
      if(chip)chip.textContent="✅ 다음 전체 청소 준비 완료";
      setGuide(state.batteryStrategy==="ready"?"청소 준비 우선 모드로 여유 있게 준비됐어요.":"다음 전체 청소에 필요한 만큼 준비됐어요.","done");
      showToast(state.batteryStrategy==="ready"?"청소 준비 완료! 여유 있게 준비해뒀어요.":"다음 청소 준비 완료! 필요한 만큼 채워뒀어요.");
    }else{
      if(speech)speech.innerHTML="<strong>배불러요!</strong><br>이제 "+state.selectedLabel+" 청소가 가능해요.";
      if(chip)chip.textContent="💖 출동 준비 완료";
      setGuide("이미 충분히 준비됐어요. 바로 청소를 시작할 수 있어요.","done");
      showToast("이미 충분히 준비됐어요. 바로 출동할 수 있어요.");
    }
    setTimeout(()=>{state.chargeComplete=false;render()},2600);
    return;
  }
  closeModal();
  switchPage("homePage");
  state.charging=true;
  startChargingSound();
  state.robotMotion='returning';
  state.chargeComplete=false;
  render();
  if(isNextHomeCharge){
    setGuide(state.batteryStrategy==="ready"?"청소 준비 우선 모드로 최대 충전 상한까지 여유 있게 준비하고 있어요.":"다음 청소에 필요한 만큼만 미리 충전하고 있어요.","charging");
    showToast(state.batteryStrategy==="ready"?"다음 청소를 위해 여유 있게 미리 준비할게요.":"다음 청소에 필요한 만큼만 미리 충전할게요.");
  }else{
    setGuide("홈지니가 스테이션으로 돌아가고 있어요. 필요한 만큼만 충전하고 출발할게요.","charging");
    showToast("스테이션으로 돌아가 힘을 채울게요.");
  }
  setTimeout(()=>{state.robotMotion='docked';render();},950);
  setTimeout(()=>{
  const timer=setInterval(()=>{
    state.soc=Math.min(state.targetSoc,state.soc+2);
    state.temperature=Math.min(32,state.temperature+.1);
    spawnEffect("⚡",2);
    render();
    if(state.soc>=state.targetSoc){
      clearInterval(timer);
      state.charging=false;
      stopChargingSound();
      playChargingCompleteSound();
      state.robotMotion='docked';
      state.temperature=29;
      state.acceptCount+=1;
      ensureWeeklyBatteryHabit().smartCharge+=1;
      saveWeeklyBatteryHabit();
      if(isNextHomeCharge)state.nextHomeReady=true;
      // [부품케어 탭 연동] 덜 채운 충전량 누적 + 수명 보호 기록
      state.savedChargePct+=Math.max(0,100-state.targetSoc);
      state.chargeComplete=true;
      if(isNextHomeCharge){
        if(state.batteryStrategy==="ready")
          addEvent("청소 준비 우선 충전 완료","청소 후 최대 충전 상한까지 여유 있게 준비해 다음 청소에 대비했어요.","여유 준비");
        else
          addEvent("다음 청소 준비 완료","다음 청소에 필요한 만큼만 미리 충전해 준비했어요.","맞춤 준비");
      }else{
        addEvent("맞춤 충전 완료",state.selectedLabel+" 청소에 필요한 만큼만 충전하고 멈췄어요. 불필요한 완충을 줄여 배터리를 보호했어요.","배터리 보호");
      }
      spawnEffect("💖",12);
      spawnEffect("✨",8);
      render();
      const speech=$("speech");
      const chip=$("modeChip");
      if(isNextHomeCharge){
        if(speech)speech.innerHTML=state.batteryStrategy==="ready"
          ? "<strong style='color:#2f8b3a'>청소 준비 완료!</strong><br>여유 있게 미리 준비해뒀어요."
          : "<strong style='color:#2f8b3a'>다음 청소 준비 완료!</strong><br>필요한 만큼 채워뒀어요.";
        if(chip)chip.textContent="✅ 다음 전체 청소 준비 완료";
        setGuide(state.batteryStrategy==="ready"?"청소 준비 우선 모드로 여유 있게 준비됐어요.":"다음 청소에 필요한 만큼 미리 준비됐어요.","done");
        showToast(state.batteryStrategy==="ready"?"청소 준비 완료! 여유 있게 준비해뒀어요.":"다음 청소 준비 완료! 필요한 만큼 채워뒀어요.");
      }else{
        if(speech)speech.innerHTML="<strong>배불러요!</strong><br>출동할 준비가 됐어요!";
        if(chip)chip.textContent="💖 충전 완료 · 출동 준비";
        setGuide("충전 완료! 홈지니가 곧 바로 출동할게요.","done");
        showToast("충전 완료! 이제 홈지니가 출동할 수 있어요.");
      }
      setTimeout(()=>{state.chargeComplete=false;render()},3200);
      if(autoStart){setTimeout(()=>{state.robotMotion='departing';render();setTimeout(()=>{state.robotMotion='idle';startCleaning();},850)},900)}
      else setTimeout(checkMissionUnlock,3600);
    }
  },150);
  },1050);
}
function buyFood(){
  if(state.coins<50){showToast("코인이 조금 부족해요. 청소 미션으로 코인을 모아보세요.");return}
  state.coins-=50;
  state.food+=1;
  render();
  showToast("냠냠! 에너지 간식 1개를 챙겼어요. 필요할 때 먹여주세요.");
}
function handleRewardItem(key){
  const item=shopItems[key];
  if(!item)return;
  if(!state.ownedItems[key]){
    if(state.coins<item.cost){
      showToast(item.name+"을(를) 데려오려면 코인이 조금 더 필요해요.");
      return;
    }
    state.coins-=item.cost;
    state.ownedItems[key]=true;
    state.equippedItems[item.slot]=item.value;
    saveCloset();
    switchPage("homePage");
    setTimeout(()=>{spawnEffect(item.icon,10);showToast(item.message);render();},250);
    render();
    return;
  }
  const isEquipped=state.equippedItems[item.slot]===item.value;
  if(isEquipped){
    state.equippedItems[item.slot]=(item.slot==="head"?"crown":null);
    saveCloset();
    render();
    showToast(item.name+"을(를) 잠시 벗겨뒀어요.");
  }else{
    state.equippedItems[item.slot]=item.value;
    saveCloset();
    switchPage("homePage");
    setTimeout(()=>{spawnEffect(item.icon,8);showToast(item.message);render();},250);
    render();
  }
}

function switchRewardTab(tab){
  state.rewardTab=tab;
  render();
}
function handleCoupon(key){
  const item=couponItems[key];
  if(!item)return;
  if(state.coins<item.cost){
    const need=Math.max(0,item.cost-state.coins);
    showToast(item.name+" 교환까지 "+need+"코인 더 필요해요.");
    return;
  }
  state.coins-=item.cost;
  state.ownedCoupons[key]=Number(state.ownedCoupons[key]||0)+1;
  saveCoupons();
  render();
  showToast(item.message+" 혜택: "+item.benefit);
}


const actions={
  startFirstMapping:startFirstMapping,
  predictSoc:predictSocFromConditions,
  executeTopClean:executeTopClean,
  manualCleanAndGo:manualCleanAndGo,
  aiAutoClean:aiAutoClean,dirtyOnlyClean:dirtyOnlyClean,toggleNoGoMode:toggleNoGoMode,mapZone:handleMapZoneTap,
  batteryStrategyCare:()=>setBatteryStrategy("care"),batteryStrategyReady:()=>setBatteryStrategy("ready"),
  selectHome:()=>selectScenario("home"),selectZone1:()=>selectScenario("zone",1),selectZone2:()=>selectScenario("zone",2),selectZone3:()=>selectScenario("zone",3),selectZone4:()=>selectScenario("zone",4),selectZone5:()=>selectScenario("zone",5),selectZone6:()=>selectScenario("zone",6),selectZone7:()=>selectScenario("zone",7),selectZone8:()=>selectScenario("zone",8),
  pet:petRobot,feed:feedRobot,play:playRobot,train:trainRobot,photo:takePhoto,clean:startCleaning,charge:chargeRobot,status:showStatus,batteryCoachInfo:openBatteryCoachInfo,batteryLifeInfo:openBatteryLifeInfo,
  // 홈의 "청소 기록" 버튼은 실시간 케어 기록이 있는 부품 케어 탭으로 이동합니다.
  record:()=>switchPage("batteryPage"),care:()=>switchPage("batteryPage"),event:()=>switchPage("eventPage"),decorate:decorateRobot,shop:()=>switchPage("rewardPage"),chargeFromBattery:()=>{switchPage("homePage");setTimeout(chargeRobot,220)},
  itemSanta:()=>handleRewardItem("santa"),itemRibbon:()=>handleRewardItem("ribbon"),itemHat:()=>handleRewardItem("hat"),itemBunny:()=>handleRewardItem("bunny"),itemCat:()=>handleRewardItem("cat"),itemSparkle:()=>handleRewardItem("sparkle"),
  rewardTabItems:()=>switchRewardTab("items"),rewardTabCoupons:()=>switchRewardTab("coupons"),
  couponLg5:()=>handleCoupon("lg5"),couponCleanKit:()=>handleCoupon("cleanKit"),couponBatteryCare:()=>handleCoupon("batteryCare"),couponMoveIn:()=>handleCoupon("moveIn"),
  ribbon:()=>handleRewardItem("ribbon"),sparkle:()=>handleRewardItem("sparkle"),hat:()=>handleRewardItem("hat"),
  // ---- 2번째 탭: 부품 케어 ----
  partDetail:openPartDetail,
  // ---- 3번째 탭: 예약 청소 ----
  toggleCommute:toggleCommute,toggleDay:toggleDay,commuteMode:setCommuteMode,toggleTheme:toggleTheme,
  // ---- 4번째 탭: 이벤트 ----
  evTabFound:()=>switchEventTab("found"),evTabMission:()=>switchEventTab("mission"),evTabPhoto:()=>switchEventTab("photo"),
  foundItem:openFoundItem,foundMapBig:openFoundMapBig,claimMission:claimMission,photoOpen:openPhoto
};

document.addEventListener("click",(event)=>{const nav=event.target.closest("[data-page]");if(nav){switchPage(nav.dataset.page);return}const action=event.target.closest("[data-action]");if(action&&typeof actions[action.dataset.action]==="function"){actions[action.dataset.action](action,event)}});
// 1회차 학습 청소는 핵심 CTA라서, 이벤트 위임/터치/겹침 이슈가 있어도 반드시 동작하도록 여러 경로로 직접 연결합니다.
let lastLearnClickAt=0;
function triggerLearnButton(event){
  if(event){
    event.preventDefault();
    event.stopPropagation();
    if(event.stopImmediatePropagation)event.stopImmediatePropagation();
  }
  const now=Date.now();
  if(now-lastLearnClickAt<700)return;
  lastLearnClickAt=now;
  if(typeof startFirstMapping==="function")startFirstMapping();
}
window.__forceStartFirstMapping=triggerLearnButton;
const learnBtnDirect=$("learnBtn");
if(learnBtnDirect){
  learnBtnDirect.onclick=triggerLearnButton;
  learnBtnDirect.onpointerdown=triggerLearnButton;
  learnBtnDirect.onmousedown=triggerLearnButton;
  learnBtnDirect.ontouchstart=triggerLearnButton;
  learnBtnDirect.addEventListener("click",triggerLearnButton,true);
  learnBtnDirect.addEventListener("pointerdown",triggerLearnButton,true);
  learnBtnDirect.addEventListener("pointerup",triggerLearnButton,true);
  learnBtnDirect.addEventListener("mousedown",triggerLearnButton,true);
  learnBtnDirect.addEventListener("touchstart",triggerLearnButton,{capture:true,passive:false});
  learnBtnDirect.addEventListener("touchend",triggerLearnButton,{capture:true,passive:false});
}
document.addEventListener("pointerdown",(event)=>{
  const btn=event.target && event.target.closest ? event.target.closest("#learnBtn") : null;
  if(btn)triggerLearnButton(event);
},true);
document.addEventListener("touchstart",(event)=>{
  const target=event.target;
  const btn=target && target.closest ? target.closest("#learnBtn") : null;
  if(btn)triggerLearnButton(event);
},{capture:true,passive:false});

$("modalCancel").addEventListener("click",closeModal);$("modalConfirm").addEventListener("click",()=>modalConfirmHandler());$("modal").addEventListener("click",(event)=>{if(event.target===$("modal"))closeModal()});
["scopeSelect","cleanModeSelect","intensitySelect","todayStateSelect"].forEach(id=>{
  const el=$(id);
  if(el)el.addEventListener("change",()=>{
    if(state.profileReady && state.predicted){
      state.predicted=false;
      const loading=$('predictLoading');
      if(loading)loading.textContent="조건이 바뀌었어요. 오늘 청소 준비하기를 다시 눌러주세요.";
      render();
    }
  });
});
["leaveTime","returnTime"].forEach(id=>{const el=$(id);if(el)el.addEventListener("change",()=>render());});

setInterval(()=>{if(state.cleaning||state.charging||state.celebrating)return;const robot=$("robot");robot.classList.remove("look-left","look-right");const d=Math.random();if(d<.33)robot.classList.add("look-left");else if(d<.66)robot.classList.add("look-right");setTimeout(()=>robot.classList.remove("look-left","look-right"),1100)},2800);

fillTimeSelects();
populateConditionSelectors();
renderFound();
renderPhotos();
render();
state.notifiedClaimable=claimableCount();
</script>
</body>
</html>
"""

APP_HTML = APP_HTML.replace("__UI_PREDICTION_DATA__", UI_PREDICTION_JSON)
APP_HTML = APP_HTML.replace("__UI_MEDIA_DATA__", UI_MEDIA_JSON)
APP_HTML = APP_HTML.replace("__SANTA_HAT_DATA_URI__", SANTA_HAT_DATA_URI)

components.html(APP_HTML, height=1010, scrolling=False)
