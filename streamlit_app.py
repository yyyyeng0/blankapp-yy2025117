import streamlit as st
import random

st.set_page_config(page_title="Dice Roller", page_icon="🎲")

st.title("� 주사위 굴리기 앱")
st.write("간단한 주사위 굴리기 시뮬레이터입니다. 주사위 개수와 면수를 선택하고 '굴리기' 버튼을 누르세요.")


def face_emoji(value, sides):
    # 6면 주사위는 유니코드 주사위 이모지로 보여줍니다. 그 외는 숫자로 표시.
    if sides == 6:
        # ⚀..⚅ : U+2680..U+2685
        base = 0x2680
        try:
            return chr(base + (value - 1))
        except Exception:
            return str(value)
    return str(value)


if 'history' not in st.session_state:
    st.session_state.history = []  # 최근 굴린 기록(새로운 항목이 앞에 온다)

col1, col2 = st.columns([3, 1])
with col1:
    num_dice = st.slider("주사위 개수", min_value=1, max_value=10, value=2)
    sides = st.selectbox("주사위 면 수", options=[4, 6, 8, 10, 12, 20], index=1)
with col2:
    roll_btn = st.button("굴리기 🎯")
    clear_btn = st.button("기록 지우기 🧹")

if clear_btn:
    st.session_state.history = []

if roll_btn:
    results = [random.randint(1, sides) for _ in range(num_dice)]
    total = sum(results)
    entry = {"num": num_dice, "sides": sides, "results": results, "total": total}
    st.session_state.history.insert(0, entry)

    st.subheader("지금 굴린 결과")
    cols = st.columns(len(results))
    for i, r in enumerate(results):
        with cols[i]:
            st.markdown(f"### {face_emoji(r, sides)}")
            st.caption(f"{r}")

    st.markdown(f"**합계:** {total}")

if not roll_btn and st.session_state.history:
    # 마지막 기록(가장 최근)을 요약해서 보여줌
    last = st.session_state.history[0]
    st.subheader("마지막 굴림(요약)")
    st.write(f"{last['num']}개의 {last['sides']}면 주사위 → 합계: {last['total']}")
    row = st.columns(len(last['results']))
    for i, r in enumerate(last['results']):
        with row[i]:
            st.markdown(f"**{face_emoji(r, last['sides'])}**")

if st.session_state.history:
    with st.expander("굴림 기록 보기"):
        for i, e in enumerate(st.session_state.history):
            st.markdown(f"**#{i+1}** — {e['num']} x {e['sides']}면 주사위  → 합계: {e['total']}")
            st.write("결과: ", ", ".join(str(x) for x in e['results']))
            st.divider()

st.write("\n---\nMade with Streamlit")
