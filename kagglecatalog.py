
# Kaggle API documewntation: https://github.com/Kaggle/kaggle-api/blob/main/kaggle/api/kaggle_api_extended.py#L274
# Python scipting mention: https://stackoverflow.com/questions/78638963/how-to-list-all-files-from-a-kaggle-dataset-in-google-colab


import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import os

# Initialize and authenticate with Kaggle API
api = KaggleApi()
api.authenticate()

# Custom search term for dataset names
search_terms = ["crop disease", 'plant disease', 'leaf disease']

# List to store dataset information
data = []

# Pagination settings
page = 1
for search_term in search_terms:
    while True:
        print(f'Loading page {page} ...')

        # Fetch datasets with the custom search term
        result = api.dataset_list(search=search_term, page=page)
        
        # Check if results are empty, meaning no more datasets are available
        if not result:
            break
        
        # Extract datasets information
        for dataset in result:
            # if not os.path.exists(dataset.title):
            #     os.makedirs(dataset.title)
            
            # metadata = api.dataset_metadata(dataset.ref, dataset.title)
            # data.append([dataset.ref, dataset.title, dataset.size])
            data.append(dataset.ref)
        
        # Increment the page number to fetch the next set of results
        page += 1

# Display the datasets information
print(f"Total datasets found: {len(data)}")

unique_items = []
[unique_items.append(x) for x in data if x not in unique_items]

print(f"Total unique datasets found: {len(unique_items)}")

for index, ref in enumerate(unique_items):
    print(f'https://www.kaggle.com/datasets/{ref}')
    # print(title)


# https://www.kaggle.com/datasets/nafishamoin/new-bangladeshi-crop-disease