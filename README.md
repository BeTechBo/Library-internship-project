# AUC Library Facial Recognition Tool

## Overview

This repository contains the implementation of an image face tagging tool. The tool allows users to tag individual faces in a set of images and manage these tags effectively.

## Upcoming Features

1. **Graphical User Interface (GUI)**: A user-friendly interface for tagging faces in images.
2. **Metadata Storage**: Save identifications in separate metadata files for each image.
3. **Tag Cascading**: Automatically apply tags to all other images in the collection where the same face appears.

## Task List

- [x] Experimentation with different tools
- [x] Connect to database
- [x] Create Design for pages
- [x] Starting Page
- [x] "Unlabeled" page
- [x] "Already labeled" page
- [x] Swap page to file upload
- [x] File upload selection
- [x] Swap page to labeling
- [x] Moving between pages
- [x] Unify the qt versions
- [x] Labeling picures (UI only)
- [x] Reorganize files
- [x] Fix circular imports problem
- [x] Remove duplicates
- [x] Labelling pictures
- [x] Implement Cascading
- [x] Create Executable
- [x] More advanced removal of duplicates
- [x] Delete image option
- [x] Store images in folder
- [ ] Upload images to a folder [ Andrew ]
- [ ] Create Notebook for collab and migrate code [ Omar ]
- [ ] Migrate database to spreadsheets [ Ashkar ](partially done)
- [ ]  Make styling nicer [ Omar ]
- [ ] Fix known bugs [ Ebram ]
- [ ] Uploading photos enhancment [ Ebram ]
- [ ] View Labeled Images backend
- [ ] Automate existing spreadsheets [ Omar ]
- [ ] Implement the search method for the labelled page 
- [ ] Testing
- [ ] Installation Steps
## Some problems we need to take care of 

- When adding a lot of pictures the application became much slower (I am not sure how it will perform when we add much more images)
- These is an eror when we update the names. When I update someone name and apply cascading that happens but the name shown on the green box is not updated(need more testing on other devices . Maybe I have something in the database that is not managed correctly)
