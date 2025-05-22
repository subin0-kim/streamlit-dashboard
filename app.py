import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from typing import List

import db

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

def load_csv(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df


def list_files(search: str = ""):
    rows = db.get_files(search)
    files = []
    for row in rows:
        filepath = data_dir / row[1]
        size = filepath.stat().st_size if filepath.exists() else 0
        files.append({
            "id": row[0],
            "filename": row[1],
            "alias": row[2],
            "description": row[3],
            "uploaded_at": row[4],
            "size": size,
        })
    return files


def sidebar_file_selector() -> List[int]:
    st.sidebar.header("Available Files")
    search = st.sidebar.text_input("File Search")
    files = list_files(search)
    selected_ids = []
    for f in files:
        tooltip = f["description"] if f["description"] else f["filename"]
        checked = st.sidebar.checkbox(f["alias"], key=f"file_{f['id']}", help=tooltip)
        if checked:
            selected_ids.append(f["id"])
    return selected_ids


def sidebar_goodput_settings() -> dict:
    with st.sidebar.expander("Goodput Settings"):
        ttft = st.number_input("TTFT", value=3.0)
        tpot = st.number_input("TPOT", value=0.2)
    return {"TTFT": ttft, "TPOT": tpot}


def sidebar_upload():
    with st.sidebar.expander("File Upload"):
        uploaded_files = st.file_uploader("Upload CSV", type="csv", accept_multiple_files=True)
        for uploaded in uploaded_files or []:
            filepath = data_dir / uploaded.name
            with open(filepath, "wb") as f:
                f.write(uploaded.getbuffer())
            db.add_file(uploaded.name, alias=uploaded.name.rsplit(".",1)[0])
        if uploaded_files:
            st.success("File uploaded")


def show_metrics(df: pd.DataFrame, metric: str, goodput: dict):
    filtered = df[(df["First Token"] <= goodput["TTFT"]) & (df["decode"] <= goodput["TPOT"])]
    if filtered.empty:
        st.write("No data matching goodput conditions")
        return

    if metric == "TPM":
        max_val = filtered["TPM"].max()
        fig = px.bar(filtered, x="BATCH", y="TPM", text="TPM")
        fig.update_traces(texttemplate="%{text:.0f}")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Performance Summary - TPM"):
            st.dataframe(filtered[["BATCH", "TPM"]])
        st.caption(f"Max TPM: {max_val}")
    elif metric == "RPM":
        max_val = filtered["RPM"].max()
        fig = px.bar(filtered, x="BATCH", y="RPM", text="RPM")
        fig.update_traces(texttemplate="%{text:.0f}")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Performance Summary - RPM"):
            st.dataframe(filtered[["BATCH", "RPM"]])
        st.caption(f"Max RPM: {max_val}")
    elif metric == "TPM Trend":
        fig = px.line(df, x="BATCH", y="TPM")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Performance Summary - TPM Trend"):
            st.dataframe(df[["BATCH", "TPM"]])
    elif metric == "RPM Trend":
        fig = px.line(df, x="BATCH", y="RPM")
        st.plotly_chart(fig, use_container_width=True)
        with st.expander("Performance Summary - RPM Trend"):
            st.dataframe(df[["BATCH", "RPM"]])


def dashboard_page():
    selected_files = sidebar_file_selector()
    goodput = sidebar_goodput_settings()
    sidebar_upload()

    metrics = ["TPM", "TPM Trend", "RPM", "RPM Trend"]
    chosen_metrics = st.multiselect("Metrics", metrics, default=["TPM"])

    if not selected_files:
        st.info("Select at least one file")
        return

    for fid in selected_files:
        file_row = next((f for f in list_files() if f["id"] == fid), None)
        if not file_row:
            continue
        file_path = data_dir / file_row["filename"]
        if not file_path.exists():
            st.warning(f"File {file_row['filename']} missing")
            continue
        st.subheader(file_row["alias"])
        if file_row["description"]:
            st.caption(file_row["description"])
        df = load_csv(file_path)
        for metric in chosen_metrics:
            st.write(f"### {metric}")
            show_metrics(df, metric, goodput)


def file_management_page():
    st.header("File Upload")
    uploaded_files = st.file_uploader("Upload CSV", type="csv", accept_multiple_files=True)
    for uploaded in uploaded_files or []:
        filepath = data_dir / uploaded.name
        with open(filepath, "wb") as f:
            f.write(uploaded.getbuffer())
        alias = uploaded.name.rsplit(".", 1)[0]
        db.add_file(uploaded.name, alias=alias)
    if uploaded_files:
        st.success("File uploaded")

    st.header("File Listing")
    files = list_files()
    df = pd.DataFrame(files)
    if not df.empty:
        df_display = df[["alias", "description", "uploaded_at", "size"]].copy()
        df_display["size_kb"] = (df_display["size"] / 1024).astype(int)
        st.dataframe(df_display[["alias", "description", "uploaded_at", "size_kb"]])

        st.subheader("Edit Metadata")
        for _, row in df.iterrows():
            with st.expander(row["alias"]):
                alias = st.text_input("Alias", row["alias"], key=f"alias_{row['id']}")
                description = st.text_area("Description", row["description"], key=f"desc_{row['id']}")
                if st.button("Update", key=f"update_{row['id']}"):
                    db.update_file(row["id"], alias, description)
                    st.success("Updated")
    else:
        st.write("No files")

    st.header("File Deletion")
    if not df.empty:
        ids = st.multiselect("Select files to delete", df["id"], format_func=lambda x: df.loc[df['id']==x, 'alias'].values[0])
        if st.button("Delete") and ids:
            for fid in ids:
                file_path = data_dir / df.loc[df['id']==fid, 'filename'].values[0]
                if file_path.exists():
                    file_path.unlink()
            db.delete_files(ids)
            st.success("Deleted")


def main():
    st.set_page_config(page_title="Performance Dashboard", layout="wide")
    db.init_db()
    page = st.sidebar.selectbox("Page", ["Dashboard", "File Management"])
    if page == "Dashboard":
        dashboard_page()
    else:
        file_management_page()


if __name__ == "__main__":
    main()
