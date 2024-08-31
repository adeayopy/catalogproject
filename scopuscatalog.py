# 4371be505eaf77e3792a20575500fb09

import os
import traceback
from pybliometrics.scopus import ScopusSearch, AbstractRetrieval
import json
from tqdm import tqdm
import pybliometrics

pybliometrics.scopus.init()

# NOTE: config file for pybliometrics is stored in $HOME/.config/pybliometrics.cfg

if __name__ == "__main__":
    for year in range(2020, 2021):
        # make the folder to store the data for the year
        current_path = os.getcwd()
        folder_path = os.path.join(current_path, "output", str(year))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # get the results
        # x = ScopusSearch(
        #     f'ABS ( "crop disease" ) OR ABS ( "plant disease" ) OR TITLE ( "disease" ) OR TITLE ( "dataset" ) AND ABS ( "dataset" ) OR ABS ( "data" ) AND SUBJAREA ( agri ) OR SUBJAREA ( engi ) AND DOCTYPE ( "AR" ) OR DOCTYPE ( "CP" ) OR DOCTYPE ( "CR" ) OR DOCTYPE ( "RE" ) AND PUBYEAR = {year} AND NOT SUBJAREA (medi ) AND NOT SUBJAREA ( immu ) AND NOT SUBJAREA ( busi )',
        #     view="STANDARD")
        x=ScopusSearch(
            f'ABS ( "plant disease" OR "crop disease" AND "dataset" OR "data" OR "disease detection" OR "disease classification" OR "disease segmentation") '
            f'OR TITLE ( "plant disease" OR "crop disease" AND "dataset" OR "data" ) '
            f'AND SUBJAREA ( agri OR engi OR envi OR comp OR bioc ) '
            f'AND DOCTYPE ( "AR" OR "CP" OR "CR" OR "RE" ) '
            f'AND PUBYEAR = {year} '
            f'AND NOT SUBJAREA ( medi OR immu OR busi OR soci OR econ OR psyc )',
            view="STANDARD"
        )

        print(f"Year: {year} , Results count: {len(x.results)}")
        for doc in tqdm(x.results):
            doc_dict = doc._asdict()
            title=doc_dict['title']
            doi=doc_dict['doi']
            publicationname=doc_dict['publicationName']
            print(title, '|',doi,'|', publicationname)
            print('-----------------------------------------------------------')
            # print(doc_dict)


        # store the results and add the ref_docs key to store each reference
        # for doc in tqdm(x.results):
        #     try:
        #         # store each result in a file labeled by its Scopus EID
        #         doc_dict = doc._asdict()
        #         eid = doc_dict["eid"]
        #         file_path = os.path.join(folder_path, f"{eid}.json")
        #         if not os.path.exists(file_path):
        #             # Look up the references / citations for that document
        #             document = AbstractRetrieval(eid, view="REF")
        #             refs = []
        #             # Store the references
        #             for ref in document.references:
        #                 ref_doc = {"doi": ref.doi, "title": ref.title,
        #                            "id": ref.id,
        #                            "sourcetitle": ref.sourcetitle}
        #                 refs.append(ref_doc)
        #             doc_dict["ref_docs"] = refs
        #             # Dump the dictionary to the JSON file
        #             with open(file_path, "w") as json_file:
        #                 json.dump(doc_dict, json_file)
        #         else:
        #             print("SKIP (File already exists)")

        #     # we're not going to try too hard to fix any of the rare errors
        #     except Exception as e:
        #         pass
        #         # print(f"An error occurred: {e}")
        #         # traceback.print_exc()
