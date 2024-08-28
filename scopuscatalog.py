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
    for year in range(2020, 2024):
        # make the folder to store the data for the year
        current_path = os.getcwd()
        folder_path = os.path.join(current_path, "output", str(year))
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # get the results
        x = ScopusSearch(
            f'ABS ( "crop disease dataset" ) OR ABS ( "plant disease dataset" ) OR TITLE ( "plant disease dataset"" ) OR TITLE ( "crop disease dataset" ) OR SRCTITLE ( "agriculture" ) OR SRCTITLE ( "engineering" ) AND SUBJAREA ( AGRI ) OR SUBJAREA ( ENGI ) AND PUBYEAR = {year} AND NOT SUBJAREA (medi ) AND NOT SUBJAREA ( immu ) AND NOT SUBJAREA ( BIOC ) AND NOT SUBJAREA ( busi )',
            view="STANDARD")
            #  f'ABS ( "crop disease dataset" ) OR ABS ( "plant disease dataset" ) OR TITLE ( "plant disease dataset"" ) OR TITLE ( "crop disease dataset" ) AND TITLE ( "material" ) OR ABS ( "material" ) OR SRCTITLE ( "material" ) AND SUBJAREA ( mate ) AND DOCTYPE ( "AR" ) AND SRCTYPE( j ) AND PUBYEAR = {year} AND NOT SUBJAREA (medi ) AND NOT SUBJAREA ( immu ) AND NOT SUBJAREA ( BIOC ) AND NOT SUBJAREA ( busi )',
            # view="STANDARD")
        print(f"Year: {year} , Results count: {len(x.results)}")

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
