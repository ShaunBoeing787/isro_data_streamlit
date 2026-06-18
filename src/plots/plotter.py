from plotly.subplots import make_subplots
import plotly.graph_objects as go


def build_dashboard(
    solex_df,
    hel_df
):

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=(
            "SoLEXS Soft X-Ray",
            "HEL1OS Hard X-Ray"
        )
    )

    # SoLEXS

    fig.add_trace(
        go.Scatter(
            x=solex_df["datetime"],
            y=solex_df["counts"],
            mode="lines",
            name="SoLEXS"
        ),
        row=1,
        col=1
    )

    # HEL1OS

    fig.add_trace(
        go.Scatter(
            x=hel_df["datetime"],
            y=hel_df["counts"],
            mode="lines",
            name="HEL1OS"
        ),
        row=2,
        col=1
    )

    fig.update_layout(
        height=900,
        showlegend=True,
        hovermode="x unified"
    )

    fig.update_yaxes(
        title_text="Counts/sec",
        row=1,
        col=1
    )

    fig.update_yaxes(
        title_text="Counts/sec",
        row=2,
        col=1
    )

    fig.update_xaxes(
        title_text="UTC Time",
        row=2,
        col=1
    )

    return fig