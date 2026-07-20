import pandas as pd

from services.opportunity_service import get_all_opportunities


def export_opportunities():

    rows = get_all_opportunities()

    if len(rows) == 0:
        return None

    df = pd.DataFrame([dict(r) for r in rows])

    filename = "opportunities_export.csv"

    df.to_csv(
        filename,
        index=False
    )

    return filename