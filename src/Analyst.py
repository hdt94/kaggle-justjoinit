import pandas as pd

from readings import read_data_dir
from transformations import (
    get_city_counts,
    get_salary_mean,
    filter_jobs_by_company,
    filter_jobs_by_country,
    filter_jobs_by_dates,
    filter_jobs_by_experience,
    preprocess_jobs,
)


class Analyst:
    def __init__(self):
        self.employments_types = None
        self.jobs = None
        self.multilocations = None
        self.skills = None

        self.jobs_raw = None

    def read_data_dir(self, data_dir: str = None, prefix: str = "small", n: int = 3):
        data = read_data_dir(data_dir, prefix)
        for dataset, df in data.items():
            self.__dict__[dataset] = df

        self.jobs = (
            preprocess_jobs(self.jobs)
            .sort_values("published_at", ascending=False)
        )

        assert isinstance(n, int), f'invalid n type: "{type(n)}"'
        assert n > 0, f"n lower than zero: {n}"
        assert (n * 2) <= len(self.jobs), f"exceeds number of jobs: n={n}"

        fields = [
            "published_at",
            "title",
            "company_name",
            "experience_level",
            "country_code",
            "city",
        ]
        first_jobs = self.jobs[-n:][fields].fillna("Unknown")
        last_jobs = self.jobs[:n][fields].fillna("Unknown")

        return {
            "count_jobs": len(self.jobs),
            "records_first_jobs": first_jobs.to_dict(orient="records"),
            "records_latest_jobs": last_jobs.to_dict(orient="records"),
        }

    def requirement_1(self, n: int, country: str, experience: str):
        assert isinstance(n, int), f'invalid n type: "{type(n)}"'
        assert n > 0, f"n lower than zero: {n}"

        df = self.jobs.copy()
        df = filter_jobs_by_experience(df, experience)
        count_jobs_experience = len(df)

        df = filter_jobs_by_country(df, country)
        count_jobs_experience_country = len(df)

        fields = [
            "published_at",
            "title",
            "company_name",
            "experience_level",
            "country_code",
            "city",
            "company_size",
            "open_to_hire_ukrainians",
        ]

        return {
            f"count_jobs_{experience}": count_jobs_experience,
            f"count_jobs_{experience}_{country}": count_jobs_experience_country,
            "records": df[fields].head(n).to_dict(orient="records"),
        }

    def requirement_2(self, company: str, start_date: str, end_date: str):
        df = self.jobs.copy()
        df = filter_jobs_by_company(df, company)
        df = filter_jobs_by_dates(df, start_date, end_date)

        experience_counts = df["experience_level"].value_counts()

        fields = [
            "published_at",
            "title",
            "experience_level",
            "city",
            "country_code",
            "company_size",
            "workplace_type",
            "open_to_hire_ukrainians",
        ]

        return {
            "count_jobs": len(df),
            "count_jobs_junior": experience_counts.get("junior", 0),
            "count_jobs_mid": experience_counts.get("mid", 0),
            "count_jobs_senior": experience_counts.get("senior", 0),
            "records": df[fields].to_dict(orient="records")
        }

    def requirement_3(self, country: str, start_date: str, end_date: str):
        df = self.jobs.copy()
        df = filter_jobs_by_country(df, country)
        df = filter_jobs_by_dates(df, start_date, end_date)
        df["remote"] = df["workplace_type"] == "remote"

        city_counts = get_city_counts(df, self.employments_types)

        fields = [
            "published_at",
            "title",
            "experience_level",
            "company_name",
            "city",
            "workplace_type",
            "remote",
            "open_to_hire_ukrainians",
        ]

        return {
            "count_jobs": len(df),
            "count_companies": df["company_name"].nunique(),
            "count_cities": len(city_counts),
            "city_least_jobs": city_counts.index[-1],
            "city_most_jobs": city_counts.index[0],
            "records": df[fields].to_dict(orient="records")
        }

    def requirement_4(self, n: int, start_date: str, end_date: str, experience: str, country: str = None):
        def aggregate_per_city(df: pd.DataFrame):
            companies_counts = df["company_name"].value_counts(ascending=False)

            ncurrencies = df["currency_salary"].nunique()
            if (ncurrencies > 1):
                currencies = df["currency_salary"].nunique.values.tolist()
                raise ValueError(f"multiple currencies in city: {currencies}")

            return pd.Series({
                "count_jobs": len(df),
                "count_companies": len(companies_counts),
                "most_jobs_company_count": companies_counts[0],
                "most_jobs_company_name": companies_counts.index[0],
                "salary_best": df["salary_to"].max(),
                "salary_mean": get_salary_mean(df),
                "salary_worst": df["salary_from"].min(),
            })

        df = self.jobs.copy()
        df = filter_jobs_by_dates(df, start_date, end_date)
        df = filter_jobs_by_experience(df, experience)
        df = pd.merge(df, self.employments_types, on="id", how="left")

        assert isinstance(n, int), f'invalid n type: "{type(n)}"'
        assert n > 0, f"n lower than zero: {n}"
        df = df.head(n)

        city_counts = get_city_counts(df, self.employments_types)
        count_companies = df["company_name"].nunique()

        fields = [
            "city",
            "company_name",
            "currency_salary",
            "salary_to",
            "salary_from",
        ]
        aggs_per_city = df.groupby("city")[fields].apply(aggregate_per_city)

        return {
            "count_cities": len(aggs_per_city),
            "count_companies": count_companies,
            "count_jobs": len(df),
            "least_jobs_city_count": city_counts[-1],
            "least_jobs_city_name": city_counts.index[-1],
            "most_jobs_city_count": city_counts[0],
            "most_jobs_city_name": city_counts.index[0],
            "salary_mean": None if country is None else get_salary_mean(df),
            "records": aggs_per_city.to_dict(orient="records"),
        }

    def requirement_5(self, n: int, start_date: str, end_date: str):
        jobs_fields = ["city", "company_name",
                       "country_code", "experience_level", "id"]
        multilocations_renaming = {"city": "city_locations"}
        skills_renaming = {"name": "skill_name", "level": "skill_level"}

        def get_location_stats(df: pd.DataFrame):
            # idx = ~(df["city"].isna()) | ~(df["city_locations"].isna())
            idx = df["city"].notna() | df["city_locations"].notna()

            return {
                "count_companies_with_location": df["company_name"][idx].nunique(),
                "count_companies_without_location": df["company_name"][~idx].nunique()
            }

        def get_skills_stats(df: pd.DataFrame):
            companies_counts = df["company_name"].value_counts(ascending=False)
            skills_counts = df["skill_name"].value_counts(ascending=False)

            return {
                "count_unique_skills": len(skills_counts),
                "most_required_skill_count": skills_counts[0],
                "most_required_skill_name": skills_counts.index[0],
                "least_required_skill_count": skills_counts[-1],
                "least_required_skill_name": skills_counts.index[-1],
                "minimum_skills_level": df["skill_level"].mean(),
                "count_companies": len(companies_counts),
                "most_jobs_company_count": companies_counts[0],
                "most_jobs_company_name": companies_counts.index[0],
                "least_jobs_company_count": companies_counts[-1],
                "least_jobs_company_name": companies_counts.index[-1],
            }

        assert isinstance(n, int), f'invalid n type: "{type(n)}"'
        assert n > 0, f"n lower than zero: {n}"

        top_countries_counts = (
            self.jobs["country_code"]
            .value_counts(ascending=False)
            .head(n)
        )
        top_countries = top_countries_counts.index

        top = self.jobs[jobs_fields].query("country_code in @top_countries")
        locations_stats = (
            pd.merge(
                top,
                self.multilocations.rename(columns=multilocations_renaming),
                on="id",
                how="left"
            )
            .groupby("experience_level")
            .apply(get_location_stats)
        )
        skills_stats = (
            pd.merge(
                top,
                self.skills.rename(columns=skills_renaming),
                on="id",
                how="left"
            )
            .groupby("experience_level")
            .apply(get_skills_stats)
        )

        return {
            "count_jobs": top_countries_counts.sum(),
            "count_cities": top["city"].nunique(),
            "most_jobs_country_count": top_countries_counts[0],
            "most_jobs_country_name": top_countries_counts.index[0],
            "stats_per_level": {
                level: {**locations_stats[level], **skills_stats[level]}
                for level in ["junior", "mid", "senior"]
            }
        }
