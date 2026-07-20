from database.database import get_connection


def save_opportunity(data: dict):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO opportunities
        (
            title,
            organizer,
            category,
            description,
            website,
            deadline,
            status,
            priority,
            funding_amount,
            location,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("title", ""),
            data.get("organizer", ""),
            data.get("category", ""),
            data.get("description", ""),
            data.get("website", ""),
            data.get("deadline", ""),
            "Not Started",
            "High",
            data.get("funding_amount", ""),
            data.get("location", ""),
            "",
        ),
    )

    conn.commit()
    conn.close()


def get_all_opportunities():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM opportunities
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def delete_opportunity(opportunity_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM opportunities WHERE id=?",
        (opportunity_id,)
    )

    conn.commit()
    conn.close()