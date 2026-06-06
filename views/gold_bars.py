from datetime import date

import streamlit as st

from services.portfolio_service import (
    create_bar,
    delete_bar,
    get_all_bars,
    get_bar_by_id,
    get_portfolio_metrics,
    metrics_to_dataframe,
    update_bar,
)
from utils.formatting import (
    format_date_local,
    format_money,
    format_ownership,
    format_percentage,
    format_weight,
)
from utils.privacy import is_privacy_mode
from utils.i18n import get_lang, render_empty_state, t

SORT_OPTIONS = {
    "sort_date": "purchase_date",
    "sort_profit": "profit_loss",
    "sort_value": "current_value",
    "sort_grams": "grams",
}


def _init_participant_state(key_prefix: str, initial: list[dict] | None = None) -> None:
    state_key = f"{key_prefix}_participants"
    if state_key not in st.session_state:
        st.session_state[state_key] = initial or [{"participant_name": "", "ownership_percentage": 50.0}]


def _render_participants(key_prefix: str) -> list[dict]:
    state_key = f"{key_prefix}_participants"
    participants_state = st.session_state[state_key]
    updated = []

    for i, participant in enumerate(participants_state):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            name = st.text_input(
                t("participant_name"),
                value=participant.get("participant_name", ""),
                key=f"{key_prefix}_name_{i}",
            )
        with col2:
            pct = st.number_input(
                t("ownership_pct"),
                min_value=0.0,
                max_value=100.0,
                value=float(participant.get("ownership_percentage", 0.0)),
                step=1.0,
                key=f"{key_prefix}_pct_{i}",
            )
        with col3:
            if st.button(t("remove_participant"), key=f"{key_prefix}_remove_{i}"):
                participants_state.pop(i)
                st.session_state[state_key] = participants_state
                st.rerun()
        updated.append({"participant_name": name, "ownership_percentage": pct})

    st.session_state[state_key] = updated

    if st.button(t("add_participant"), key=f"{key_prefix}_add"):
        updated.append({"participant_name": "", "ownership_percentage": 0.0})
        st.session_state[state_key] = updated
        st.rerun()

    return [p for p in updated if p["participant_name"].strip()]


def _validate_bar_form(
    purchase_date: date | None,
    purchase_price: float,
    grams: float,
    bar_type: str,
    ownership_percentage: float,
    participants: list[dict],
    is_shared: bool,
) -> str | None:
    if not purchase_date or not bar_type.strip() or purchase_price <= 0 or grams <= 0:
        return t("required_fields_error")
    if ownership_percentage < 1 or ownership_percentage > 100:
        return t("ownership_range_error")
    if is_shared and participants:
        total = sum(p["ownership_percentage"] for p in participants)
        if abs(total - 100.0) > 0.01:
            return t("participants_sum_error")
    return None


def _bar_form(key_prefix: str, bar=None) -> dict | None:
    is_edit = bar is not None
    initial_participants = None
    if bar and bar.participants:
        initial_participants = [
            {
                "participant_name": p.participant_name,
                "ownership_percentage": p.ownership_percentage,
            }
            for p in bar.participants
        ]
    _init_participant_state(key_prefix, initial_participants)

    is_shared = st.checkbox(
        t("shared_ownership"),
        value=bool(bar and bar.participants) if bar else False,
        key=f"{key_prefix}_shared",
    )

    participants = []
    if is_shared:
        st.markdown(f"**{t('participants')}**")
        participants = _render_participants(key_prefix)

    with st.form(f"{key_prefix}_form", clear_on_submit=not is_edit):
        purchase_date = st.date_input(
            t("purchase_date"),
            value=bar.purchase_date if bar else date.today(),
        )
        col1, col2 = st.columns(2)
        with col1:
            grams = st.number_input(
                t("grams"),
                min_value=0.1,
                value=float(bar.grams) if bar else 5.0,
                step=0.1,
            )
        with col2:
            purchase_price = st.number_input(
                t("purchase_price"),
                min_value=0.0,
                value=float(bar.purchase_price) if bar else 0.0,
                step=1.0,
                help=t("purchase_price_help"),
            )
        bar_type = st.text_input(
            t("bar_type"),
            value=bar.bar_type if bar else "",
        )
        ownership_percentage = st.number_input(
            t("ownership_pct"),
            min_value=1.0,
            max_value=100.0,
            value=float(bar.ownership_percentage) if bar else 100.0,
            step=1.0,
            help=t("my_share"),
        )
        notes = st.text_area(
            t("notes"),
            value=bar.notes or "" if bar else "",
        )

        submitted = st.form_submit_button(t("save"))
        if not submitted:
            return None

        error = _validate_bar_form(
            purchase_date,
            purchase_price,
            grams,
            bar_type,
            ownership_percentage,
            participants,
            is_shared,
        )
        if error:
            st.error(error)
            return None

        return {
            "purchase_date": purchase_date,
            "purchase_price": purchase_price,
            "grams": grams,
            "bar_type": bar_type.strip(),
            "ownership_percentage": ownership_percentage,
            "notes": notes.strip() or None,
            "participants": participants if is_shared else [],
        }


def render(session, gram_price: float, user_id: int) -> None:
    st.subheader(t("nav_gold_bars"))

    if is_privacy_mode():
        st.info(t("privacy_active"))

    metrics, _ = get_portfolio_metrics(session, gram_price, user_id)
    show_add_prominent = st.session_state.pop("open_add_bar", False) or not metrics

    if show_add_prominent:
        st.markdown(f"### {t('add_bar')}")
        data = _bar_form("add_prominent")
        if data:
            create_bar(session, user_id, **data)
            st.success(t("bar_added"))
            st.rerun()
        st.divider()

    tab_list, tab_add, tab_edit, tab_delete = st.tabs(
        [t("nav_gold_bars"), t("add_bar"), t("edit_bar"), t("delete_bar")]
    )

    with tab_list:
        if not metrics:
            render_empty_state(t("no_bars_title"), t("no_bars_hint"))
        else:
            df = metrics_to_dataframe(metrics)

            col_search, col_filter, col_sort = st.columns([2, 1, 1])
            with col_search:
                search = st.text_input(t("search"), key="bars_search")
            with col_filter:
                bar_types = sorted(df["bar_type"].unique().tolist())
                selected_type = st.selectbox(
                    t("filter_bar_type"),
                    [t("all_types")] + bar_types,
                    key="bars_filter",
                )
            with col_sort:
                sort_labels = list(SORT_OPTIONS.keys())
                sort_choice = st.selectbox(
                    t("sort_by"),
                    sort_labels,
                    format_func=t,
                    key="bars_sort",
                )

            filtered = df.copy()
            sort_col = SORT_OPTIONS[sort_choice]
            ascending = sort_col == "purchase_date"
            filtered = filtered.sort_values(sort_col, ascending=ascending)
            if search:
                mask = (
                    filtered["bar_type"].str.contains(search, case=False, na=False)
                    | filtered["notes"].str.contains(search, case=False, na=False)
                )
                filtered = filtered[mask]
            if selected_type != t("all_types"):
                filtered = filtered[filtered["bar_type"] == selected_type]

            display_df = filtered.rename(
                columns={
                    "purchase_date": t("purchase_date"),
                    "bar_type": t("bar_type"),
                    "grams": t("grams"),
                    "purchase_price": t("purchase_price"),
                    "cost_per_gram": t("cost_per_gram"),
                    "current_value": t("current_value"),
                    "profit_loss": t("profit_loss"),
                    "return_percentage": t("return_pct"),
                    "ownership_percentage": t("ownership_pct"),
                }
            )
            lang = get_lang()
            display_cols = [
                t("purchase_date"),
                t("bar_type"),
                t("grams"),
                t("purchase_price"),
                t("cost_per_gram"),
                t("current_value"),
                t("profit_loss"),
                t("return_pct"),
                t("ownership_pct"),
            ]
            formatted_df = display_df[display_cols].copy()
            formatted_df[t("purchase_date")] = formatted_df[t("purchase_date")].apply(
                lambda x: format_date_local(x, lang)
            )
            formatted_df[t("grams")] = formatted_df[t("grams")].apply(
                lambda x: format_weight(x, lang)
            )
            formatted_df[t("purchase_price")] = formatted_df[t("purchase_price")].apply(
                lambda x: format_money(x, lang)
            )
            formatted_df[t("cost_per_gram")] = formatted_df[t("cost_per_gram")].apply(
                lambda x: format_money(x, lang)
            )
            formatted_df[t("current_value")] = formatted_df[t("current_value")].apply(
                lambda x: format_money(x, lang)
            )
            formatted_df[t("profit_loss")] = formatted_df[t("profit_loss")].apply(
                lambda x: format_money(x, lang, signed=True)
            )
            formatted_df[t("return_pct")] = formatted_df[t("return_pct")].apply(
                format_percentage
            )
            formatted_df[t("ownership_pct")] = formatted_df[t("ownership_pct")].apply(
                format_ownership
            )
            st.dataframe(
                formatted_df,
                width="stretch",
                hide_index=True,
            )

    with tab_add:
        data = _bar_form("add")
        if data:
            create_bar(session, user_id, **data)
            st.success(t("bar_added"))
            st.rerun()

    with tab_edit:
        bars = get_all_bars(session, user_id)
        if not bars:
            st.info(t("no_bars"))
        else:
            lang = get_lang()
            if is_privacy_mode():
                bar_options = {b.bar_type: b.id for b in bars}
            else:
                bar_options = {
                    f"{b.bar_type} — {format_date_local(b.purchase_date, lang)} ({format_weight(b.grams, lang)})": b.id
                    for b in bars
                }
            selected = st.selectbox(t("select_bar_to_edit"), list(bar_options.keys()))
            bar = get_bar_by_id(session, bar_options[selected], user_id)
            if bar:
                data = _bar_form("edit", bar)
                if data:
                    update_bar(session, bar.id, user_id, **data)
                    st.success(t("bar_updated"))
                    st.rerun()

    with tab_delete:
        bars = get_all_bars(session, user_id)
        if not bars:
            st.info(t("no_bars"))
        else:
            lang = get_lang()
            if is_privacy_mode():
                bar_options = {b.bar_type: b.id for b in bars}
            else:
                bar_options = {
                    f"{b.bar_type} — {format_date_local(b.purchase_date, lang)} ({format_weight(b.grams, lang)})": b.id
                    for b in bars
                }
            selected = st.selectbox(t("select_bar_to_delete"), list(bar_options.keys()))
            st.warning(t("confirm_delete"))
            if st.button(t("delete"), type="primary"):
                delete_bar(session, bar_options[selected], user_id)
                st.success(t("bar_deleted"))
                st.rerun()
