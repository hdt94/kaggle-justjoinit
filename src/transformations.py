import pandas as pd


def filter_jobs_by_company(df: pd.DataFrame, company: str):
    assert isinstance(company, str), f'invalid company type: "{type(company)}"'

    return df.query(f'company_name == "{company}"')


def filter_jobs_by_country(df: pd.DataFrame, country: str):
    assert isinstance(country, str), f'invalid country type: "{type(country)}"'

    return df.query(f'country_code == "{country}"')


def filter_jobs_by_dates(df: pd.DataFrame, start_date: str, end_date: str):
    assert isinstance(start_date, str), "invalid start_date type"
    assert isinstance(end_date, str), "invalid end_date type"

    try:
        idx = (df["published_at"] >= start_date) & (df["published_at"] <= end_date)
    except TypeError as ex:
        raise TypeError("invalid date")

    return df[idx]


def filter_jobs_by_experience(df: pd.DataFrame, experience: str):
    assert isinstance(
        experience, str), f'invalid experience type: "{type(experience)}"'

    return df.query(f'experience_level == "{experience}"')


def get_city_counts(jobs: pd.DataFrame, employments_types: pd.DataFrame):
    def aggregate_per_city(city_jobs: pd.DataFrame):
        return pd.Series({
            "count_jobs": len(city_jobs),
            "salary_mean": get_salary_mean(city_jobs),
        })

    return (
        pd.merge(
            jobs[["city", "id"]],
            employments_types[["id", "salary_to", "salary_from"]],
            on="id",
            how="left",
        )
        .groupby("city")
        .apply(aggregate_per_city)
        .sort_values(["count_jobs", "salary_mean"], ascending=False)
        ["count_jobs"]
    )


def get_salary_mean(df: pd.DataFrame):
    salaries = pd.concat([df["salary_to"], df["salary_from"]])

    return salaries.mean()


def preprocess_jobs(df: pd.DataFrame):
    df = df.copy()
    df["published_at"] = pd.to_datetime(df["published_at"], format="ISO8601")

    text_fields = ['address_text', 'city', 'company_name', 'company_url', 'country_code',
                   'experience_level', 'id', 'marker_icon', 'street', 'title', 'workplace_type']
    df[text_fields] = df[text_fields].fillna("Unknown")

    return df
