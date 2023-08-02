import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import numpy as np
import re
import math

def get_pages(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        match = str(re.findall('.*Showing .* to .* of .* results\\n', soup.text)[0])        
        pages = math.ceil(int((match.split('of')[1].strip()).split(' ')[0])/50)
        return pages
    return None

def get_data_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        match = str(re.findall('.*for County: .*\\n', soup.text)[0])
        match = match[:-1]
        county = match.split(':')[1].strip()
        # Modify the 'find()' and 'find_all()' methods based on the structure of the table in the target website.
        table = soup.find('table', {'class': 'listing'})  # Replace 'table-class' with the actual class name of the table.

        if table:
            data = []
            rows = table.find_all('tr')
            for row in rows[1:]:  # Skip the header row
                cols = row.find_all('td')
                # Assuming the table has three columns: col1, col2, and col3.
                col1 = cols[2].text.strip()
                col2 = cols[3].text.strip()
                col3 = cols[4].text.strip()
                col4 = cols[5].text.strip()
                col5 = cols[6].text.strip()
                col6 = county
                data.append([col1, col2, col3, col4, col5, col6])
            return data
        else:
            print("Table not found on the page:", url)
    else:
        print("Failed to fetch the page:", url)

def scrape_multiple_pages(base_url, num_pages):
    all_data = []
    for county_num in tqdm(range(1, num_pages + 1)):
        #url = f"{base_url}&Idx={page_num}&searchaction=current&Idx={page_num}&searchaction=current"  # Assuming the pagination is based on query parameters like '?page='
        url = f"{base_url}&COU_ID={county_num}&DST_ID=0&firstpage=1&vStart=1&Idx=1&searchaction=current&Idx=1&searchaction=current"        
        for page in range(1, get_pages(url) + 1):
            url = f"{base_url}&COU_ID={county_num}&DST_ID=0&firstpage=1&vStart=1&Idx={page}&searchaction=current&Idx={page}&searchaction=current"
            page_data = get_data_from_page(url)
            if page_data:
                all_data.extend(page_data)
    return all_data

if __name__ == "__main__":
    # df = pd.read_excel(r"E:\Data_Science_Projects\Conversational_AI\misc\EducationDatasetnew.xlsx")
    # rand_val = np.random.random(df.shape[0])
    # online_offline_vals = []
    # for val in rand_val:
    #     if val <= 0.5:
    #         online_offline_vals.append("Online")
    #     else:
    #         online_offline_vals.append("Offline")

    # df["Mode of study"] = online_offline_vals
    # df["Course fee"] = np.random.randint(6000, 40000, size=df.shape[0])

    # rand_val = np.random.random(df.shape[0])
    # fulltime_parttime_vals = []
    # for val in rand_val:
    #     if val <= 0.5:
    #         fulltime_parttime_vals.append("Full time")
    #     else:
    #         fulltime_parttime_vals.append("Part time")

    # df["Time of study"] = fulltime_parttime_vals

    # df.to_excel(r"E:\Data_Science_Projects\Conversational_AI\misc\Dataset.xlsx", index=False)

    # print(df.head())




    # base_url = "https://www.qualifax.ie/qf/QFPublic/?Mainsec=courses&Subsec=search_courses&CRAsort=&action=search&display=&CRT_ID=0&CSH_ID=18&PREV_CSH_ID=&AdvancedKeyword=&keywords_and_titles=title&all_or_any_words=all&full_or_part_words=full&FCT_ID=&FDM_ID=&keywords=&QUA_ID=0&CTP_ID=0&COL_ID=0&RES_ID=0&points=&CRS_CODE=&CRA_ID=0&ATT_ID=0&PRV_ID=0&COU_ID=0&DST_ID=0&firstpage=1&vStart=1"
    # num_pages_to_scrape = 302
    # scraped_data = scrape_multiple_pages(base_url, num_pages_to_scrape)
    # df = pd.DataFrame(scraped_data, columns = ["Code", "Course", "Course Provider", "NFQ Level", "NFQ Classification"])

    # Display the scraped data
    # df = pd.read_excel(r"E:\Data_Science_Projects\Conversational_AI\misc\EducationDataset.xlsx")

    # base_url = "https://www.qualifax.ie/qf/QFPublic/?Mainsec=courses&Subsec=search_courses&CRAsort=&action=search&display=&CRT_ID=0&CSH_ID=18&PREV_CSH_ID=0&AdvancedKeyword=&keywords_and_titles=title&all_or_any_words=all&full_or_part_words=full&FCT_ID=&FDM_ID=&keywords=&CRT_ID=0&QUA_ID=0&CTP_ID=0&COL_ID=0&RES_ID=0&points=&CRS_CODE=&CRA_ID=0&ATT_ID=0&PRV_ID=0"
    # # https://www.qualifax.ie/qf/QFPublic/?Mainsec=courses&Subsec=search_courses&CRAsort=&action=search&display=&CRT_ID=0&CSH_ID=18&PREV_CSH_ID=0&AdvancedKeyword=&keywords_and_titles=title&all_or_any_words=all&full_or_part_words=full&FCT_ID=&FDM_ID=&keywords=&CRT_ID=0&QUA_ID=0&CTP_ID=0&COL_ID=0&RES_ID=0&points=&CRS_CODE=&CRA_ID=0&ATT_ID=0&PRV_ID=0
    # num_pages_to_scrape = 32
    # scraped_data = scrape_multiple_pages(base_url, num_pages_to_scrape)
    # df = pd.DataFrame(scraped_data, columns = ["Code", "Course", "Course Provider", "NFQ Level", "NFQ Classification", "County"])
    # df.to_excel(r"E:\Data_Science_Projects\Conversational_AI\misc\EducationDatasetnew.xlsx", index=False)

    #   15084
    
    preferred_field_of_study = "Accounting"
    preferred_mode_of_study = "Online"
    time_availability = "Full time"
    current_level_of_education = "High school"
    preferred_location = "NA"

    # temp = [preferred_field_of_study, preferred_mode_of_study, time_availability, preferred_location]

    # if current_level_of_education == "High school":
    #     req_edu_lvl = ["Level 6 NFQ", "Level 7 NFQ", "Level 6 NFQ, Level 7 NFQ", "Level 7 NFQ, Level 6 NFQ"]
        
    # elif current_level_of_education == "Under graduate":
    #     req_edu_lvl = ["Level 8 NFQ", "Level 9 NFQ", "Level 8 NFQ, Level 9 NFQ", "Level 9 NFQ, Level 8 NFQ"]

    # elif current_level_of_education == "Post graduate":
    #     req_edu_lvl = ["Level 10 NFQ"]
        
    # filters = temp

    # courses_df = pd.read_excel(r'.\misc\Courses.xlsx')
    # edu_df = pd.read_excel(r'.\misc\Dataset.xlsx')

    # filtered_courses = list(((courses_df[courses_df["Field"] == filters[0]]))["Course"])

    # if preferred_location != "NA":
    #     display_df = edu_df[(edu_df["Course"].isin(filtered_courses)) & (edu_df["Mode of study"] == filters[1]) & \
    #                         (edu_df["Time of study"] == filters[2]) & (edu_df["County"] == filters[3]) & \
    #                         (edu_df["NFQ Level"].isin(req_edu_lvl))].iloc[:5,:]
    #     # display_df = edu_df[(edu_df["Mode of study"] == filters[1])]
    #     # display_df = edu_df[(edu_df["County"] == filters[3])]
    #     # display_df = (edu_df[(edu_df["Time of study"] == filters[2])])
    #     # display_df = (edu_df[(edu_df["NFQ Level"] in req_edu_lvl)])
    # else:
    #     display_df = edu_df[(edu_df["Course"].isin(filtered_courses)) & (edu_df["Mode of study"] == filters[1]) & \
    #                         (edu_df["Time of study"] == filters[2]) & (edu_df["NFQ Level"].isin(req_edu_lvl))].iloc[:5,:]
    #     # display_df = edu_df[(edu_df["Course"] in filtered_courses)]
    #     # display_df = edu_df[(edu_df["Mode of study"] == filters[1])]
    #     # display_df = edu_df[(edu_df["Time of study"] == filters[2])]
    #     # display_df = (edu_df[(edu_df["NFQ Level"] in req_edu_lvl)]).iloc[:5,:]
    # paths = []
    # idx = 1
    # for i, row in display_df.iterrows():
    #     paths.append(f"Recommendation {idx}:")
    #     course = row["Course"]
    #     institute = row["Course Provider"]
    #     mode_of_study = row["Mode of study"]
    #     time_of_study = row["Time of study"]
    #     location = row["County"]
    #     course_fee = row["Course fee"]

    #     paths.append(f"Course : {course}")
    #     paths.append(f"Course Provider : {institute}")
    #     paths.append(f"Mode of study : {mode_of_study}")
    #     paths.append(f"Time of study : {time_of_study}")
    #     paths.append(f"County : {location}")
    #     paths.append(f"Course fee : {course_fee}\n")
    #     idx += 1
    
    #     # {"name": "Online certificate in Data Science", "provider": "Coursera", "duration": "6 months", "cost": "$1,000"},
    #     # {"name": "Master's degree in Business Administration", "provider": "Harvard University", "duration": "2 years", "cost": "$100,000"},
    # # return paths
    # educational_paths = paths
    



    temp = [preferred_field_of_study, preferred_mode_of_study, time_availability, preferred_location]

    if current_level_of_education == "High school":
        req_edu_lvl = ["Level 6 NFQ", "Level 7 NFQ", "Level 6 NFQ, Level 7 NFQ", "Level 7 NFQ, Level 6 NFQ"]
        
    elif current_level_of_education == "Under graduate":
        req_edu_lvl = ["Level 8 NFQ", "Level 9 NFQ", "Level 8 NFQ, Level 9 NFQ", "Level 9 NFQ, Level 8 NFQ"]

    elif current_level_of_education == "Post graduate":
        req_edu_lvl = ["Level 10 NFQ"]
        
    filters = temp

    courses_df = pd.read_excel(r'.\misc\Courses.xlsx')
    edu_df = pd.read_excel(r'.\misc\Dataset.xlsx')

    filtered_courses = list(((courses_df[courses_df["Field"] == filters[0]]))["Course"])

    # dispatcher.utter_message(text=f'{filtered_courses}')

    if preferred_location != "NA":
        display_df = edu_df[(edu_df["Course"].isin(filtered_courses)) & (edu_df["Mode of study"] == filters[1]) & \
                            (edu_df["Time of study"] == filters[2]) & (edu_df["County"] == filters[3]) & \
                            (edu_df["NFQ Level"].isin(req_edu_lvl))].iloc[:5,:]
    else:
        display_df = edu_df[(edu_df["Course"].isin(filtered_courses)) & (edu_df["Mode of study"] == filters[1]) & \
                            (edu_df["Time of study"] == filters[2]) & (edu_df["NFQ Level"].isin(req_edu_lvl))].iloc[:5,:]
        
        # dispatcher.utter_message(text=f'{display_df.head()}')
        
    paths = []
    idx = 1
    for i, row in display_df.iterrows():
        paths.append(f"Recommendation {idx}:")
        course = row["Course"]
        institute = row["Course Provider"]
        mode_of_study = row["Mode of study"]
        time_of_study = row["Time of study"]
        location = row["County"]
        course_fee = row["Course fee"]

        paths.append(f"Course : {course}")
        paths.append(f"Course Provider : {institute}")
        paths.append(f"Mode of study : {mode_of_study}")
        paths.append(f"Time of study : {time_of_study}")
        paths.append(f"County : {location}")
        paths.append(f"Course fee : {course_fee}\n")
        idx += 1
    
        # {"name": "Online certificate in Data Science", "provider": "Coursera", "duration": "6 months", "cost": "$1,000"},
        # {"name": "Master's degree in Business Administration", "provider": "Harvard University", "duration": "2 years", "cost": "$100,000"},
    # return paths
    educational_paths = paths

    # Placeholder for recommendation logic based on user preferences
    # educational_paths = recommendEducationalPaths(current_level_of_education, preferred_field_of_study, \
    #                                             preferred_mode_of_study, preferred_location, \
    #                                                 time_availability)

    if educational_paths:
        # Build a string representation of the recommended educational paths
        recommended_paths_string = "Please find below recommendations:\n"
        recommended_paths_string += "\n".join(["- " + path for path in educational_paths])

    print(recommended_paths_string)
    print("End")