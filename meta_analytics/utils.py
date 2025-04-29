import pandas as pd
from great_tables import GT, html, loc, style


def df_as_great_table(
    df_table: pd.DataFrame,
    title=None,
    subtitle=None,
):
    """Used by monitoring report"""
    return (
        GT(df_table)
        .tab_header(title=html(f'<div class="table-header">{title}</div>'), subtitle=subtitle)
        .cols_align(align="left", columns=[0, 1])
        .cols_align(align="right", columns=list(range(2, len(df_table.columns))))
        .opt_stylize(style=3)
        .opt_row_striping(row_striping=True)
        .opt_vertical_padding(scale=1.2)
        .opt_horizontal_padding(scale=1.0)
        .tab_options(
            table_width="100%",
            stub_background_color="snow",
            row_group_border_bottom_style="hidden",
            row_group_padding=0.5,
            row_group_background_color="snow",
            table_background_color="snow",
            table_font_size=10,
        )
        .tab_style(
            style=[style.fill(color="snow"), style.text(color="black")],
            locations=loc.body(
                columns=list(range(0, len(df_table.columns))),
                rows=list(range(0, len(df_table))),
            ),
        )
        .tab_style(
            style=[style.fill(color="lightgray"), style.text(color="black")],
            locations=loc.body(
                columns=[0],
                rows=list(range(0, len(df_table))),
            ),
        )
    )


def df_as_great_table2(
    df_table: pd.DataFrame,
    title=None,
    subtitle=None,
    rowname_col: str | None = None,
    groupname_col: str | None = None,
):
    """Used by monitoring report"""
    rowname_col = rowname_col or "label"
    groupname_col = groupname_col or "visit_code"
    return (
        GT(df_table, rowname_col=rowname_col, groupname_col=groupname_col)
        .tab_header(title=html(f'<div class="table-header">{title}</div>'), subtitle=subtitle)
        .cols_align(align="left", columns=[0, 1])
        .cols_align(align="right", columns=list(range(2, len(df_table.columns))))
        .opt_stylize(style=3)
        .opt_row_striping(row_striping=True)
        .opt_vertical_padding(scale=1.2)
        .opt_horizontal_padding(scale=1.0)
        .tab_options(
            table_width="100%",
            stub_background_color="snow",
            row_group_border_bottom_style="hidden",
            row_group_padding=0.5,
            row_group_background_color="snow",
            table_background_color="snow",
            table_font_size=10,
        )
        .tab_style(
            style=[style.fill(color="snow"), style.text(color="black")],
            locations=loc.body(
                columns=list(range(0, len(df_table.columns))),
                rows=list(range(0, len(df_table))),
            ),
        )
    )
