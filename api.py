from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv
from crypto_utils import decrypt_value

load_dotenv()

app = FastAPI(title="Network Dashboard API")

# CORS to allow frontend calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fetch_data():
    # --- Connect to DB ---
    conn = mysql.connector.connect(
        host=decrypt_value(os.getenv("DB_HOST")),
        user=decrypt_value(os.getenv("DB_USER")),
        password=decrypt_value(os.getenv("DB_PASSWORD")),
        port=int(os.getenv("DB_PORT", 3306))
    )

    # --- SQL Query ---
    query = """
    WITH Categorized_Data AS (
        SELECT
            c.ID,
            c.OpenedDate,
            v.city,
            CASE
                WHEN c.OptimizationFeedback IN ('Add Sector', 'Congested', 'Plan Site', 'Out of Scope', 'No Network issue', 'Covered', 'KPIs are fine') 
                    THEN 'Optimization'
                WHEN c.OptimizationFeedback IN ('Missing Information', 'Wrong Coordinates') 
                    THEN 'Non Network'
                WHEN c.OptimizationFeedback = 'Operation issue' 
                    THEN 'Operation'
                ELSE 'Unknown'
            END AS NetworkIndicator,
            CASE
                WHEN c.Technology IN ('LTE TDD', 'LTE FDD') THEN '4G'
                WHEN c.Technology = '2G' THEN '2G'
                WHEN c.Technology = '3G' THEN '3G'
                WHEN c.Technology = '5G' THEN '5G'
                ELSE 'Unknown'
            END AS ComplaintTech
        FROM sm3.vcustomercomplaint c
        JOIN sm3.vsite v ON v.internalname = c.site
        WHERE 
            (YEAR(c.OpenedDate) = 2025)
            OR (YEAR(c.OpenedDate) = 2024 AND WEEK(c.OpenedDate, 1) >= 7)
    ),
    Complaint_Summary AS (
        SELECT 
            CONCAT(YEAR(OpenedDate), LPAD(WEEK(OpenedDate, 1), 2, '0')) AS YEARWEEK,
            city,
            ComplaintTech AS Technology,
            COUNT(*) AS ComplaintCount
        FROM Categorized_Data
        WHERE 
            NetworkIndicator NOT IN ('Unknown', 'Non Network')
            AND ComplaintTech <> 'Unknown'
            AND city IN ('Dammam', 'Hafuf', 'Jeddah', 'Khubar', 'Madinah', 'Makkah', 'Riyadh')
        GROUP BY 
            YEARWEEK,
            city,
            ComplaintTech
    )
    SELECT
        ca.YEARWEEK,
        ca.Technology,
        ca.City,
        ca.`Cell Availability Rate %`,
        ca.Site_Unavail_TotalHours,
        ca.Cell_Unavail_TotalHours,
        ca.SiteCount_withDwnTime as siteCount,
        IFNULL(cs.ComplaintCount, 0) AS ComplaintCount
    FROM nas.CellAvail_City ca
    LEFT JOIN Complaint_Summary cs
        ON ca.YEARWEEK = cs.YEARWEEK
        AND ca.City = cs.city
        AND ca.Technology = cs.Technology
    WHERE ca.Technology IN ('2G', '3G', '4G', '5G')
    AND ca.YEARWEEK >= '202453'
    ORDER BY ca.YEARWEEK, ca.City, ca.Technology;
    """

    df = pd.read_sql(query, conn)
    conn.close()

    return df

@app.get("/data")
def get_data():
    df = fetch_data()
    return df.to_dict(orient="records")
