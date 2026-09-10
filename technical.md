# Technical path

## Repository setup

The team repository is:

https://github.com/ryanyu808/project.git

If the repository is not already present:

    cd ~/dso576
    git clone https://github.com/ryanyu808/project.git project
    cd project

If it is already present, update it with a fast-forward pull:

    cd ~/dso576/project
    git pull --ff-only

The read-only source dataset repository is copied under:

    project/dataset_neiss-sports-injuries/

## Data directory

Create the ignored download directory inside the dataset folder:

    cd ~/dso576/project/dataset_neiss-sports-injuries
    mkdir -p data

The repository already includes samples and lookup files under sample/. The complete annual workbooks belong in
data/ and should not be committed.

## Download procedure

1. Open the [CPSC NEISS query and download page](https://www.cpsc.gov/cgibin/NEISSQuery/home.aspx).
2. Select the **Researcher** affiliation.
3. Under **Archived Annual NEISS Data**, select a year and **Excel** format.
4. Click **Find Data**, then download the link labeled neissYYYY - MS - Excel.
5. Move the downloaded file into data/ without renaming it.
6. Repeat for 2023, 2024, and 2025.

The expected files are:

    data/neiss2023.xlsx
    data/neiss2024.xlsx
    data/neiss2025.xlsx

The optional tab-delimited 2025 file can also be saved in data/ for faster loading. If CPSC blocks a download,
wait before retrying; repeated refreshes can extend the block.

## Verification

From project/dataset_neiss-sports-injuries/, confirm the files exist:

    ls -lh data/neiss2023.xlsx data/neiss2024.xlsx data/neiss2025.xlsx

Before downloading, the checked-out data/ directory was present but empty. The committed sample can be checked
without any downloads using pandas and the file under sample/.

When analyzing the annual files, use all three product columns (Product_1, Product_2, and Product_3) to identify
sports cases, sum Weight for national estimates, and use Treatment_Date rather than the case number to determine
the year. Keep downloaded files out of commits.
