
![Built Using](https://img.shields.io/badge/Built%20Using-HTML,%20Javascript,%20SQL,%20AJAX,%20CGI-blue.svg)
[![Developed by:](https://img.shields.io/badge/Developed%20by:-grey)](https://github.com/saumyapo/Coral-Database/) [![Saumya Pothukuchi](https://img.shields.io/badge/Saumya_Pothukuchi-purple)](https://github.com/saumyapo) [![Johnathan Zhang](https://img.shields.io/badge/Johnathan_Zhang-yellow)](https://github.com/John2018330) [![Zachary Derse](https://img.shields.io/badge/Zachary_Derse-darkgreen)](https://github.com/zachderse) [![Grace Aboussleman](https://img.shields.io/badge/Grace_Aboussleman-darkred)](https://github.com/graceabouss)

*The website was created using data obtained from Dr. John Finnerty's lab at BU. Currently a work in progress to migrate the website off BU servers.*  

# Coral-Database
The aim of the project was to develop a website to explore, visual and filter the coral data to study an underlying patterns of survival as well as to study their growth over the years among other things.

- Background on the work carried out by the lab :
  *  From 2014-2022 Finnerty’s lab has studied coral in the Caribbean (Turneffe Atoll Marine Reserve, Belize).
  *  Recent decades have shown significant decline in coral cover on reefs in the tropics due to climate change – with many species at risk of extinction.
  *  This longitudinal study of the coral means to better understand the ecosystem dynamics taking place.
  *  Lab is currently focused on species that are able to survive in multiple environments – the data focuses on mangrove corals.

- Background on the data used for the project:
  *  Data divided into two main categories: phenotypic and variant cell format data (VCF).
  *  Phenotypic :
     -  Year (2015, 2016, 2017, 2018).
     -  Size (length, width and height).
     -   Partial mortality (alive, dead/missing).
     -  Ecological volume (also natural log of volume).
     -  Location (4 different sites).
  *  VCF :
     -  Variants determined from 2bRAD sequencing.
     -  Performed on samples collected in 2018.

## Overview of the Website

   *  Home tab: General introduction and abstract of the project.
   *  Data tab: Main tab which is used to visualise and filter the data using various options.
   *  Graphs tab: Visualising data using Google Charts.
   *  Media tab: Images hosted from the [BU Marine Program Webpage](https://bumarine.smugmug.com/) but specific to coral species.
   *  Help tab: General FAQs and guide to use the website.

<img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/b3fac7df-61d3-4a4e-81dd-56236d69d566">

 ## Data Tab
 
 <img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/a1115d55-32bf-447c-99fd-52d5ce80bf5f">

1. Filters:
   -  For each header the corresponding `Help` tab is linked in case of any questions.
   -  Wherever relevant Javascript form filling was used through examples so that users can simply click on the examples provided to fill in the input boxes.
   -  Can input Tag ID (which are the tags used to uniquely identify the corals) or Scaffold ID (which would be non-unique values present in the VCF data).
   -  The phenotypic data can be linked to the VCF data if desired by choosing Yes in the dropdown menu.
   -  The data can be sorted by a few columns present in the phenotypic data if desired. The default is sorting by year.
   -  The reset all filters button is particularly useful to quickly restore the original state of all filters.
2. Phenotypic Data Filters:
   - These are the filters for the phenotypic table (which can be used during VCF linking as well). Multiple years/locations/mortality status can be selected if desired. There are sliders present for all numerical columns. These were incorporated using the Javascript [noUiSlider](https://refreshless.com/nouislider/).
   - Each slider has a reset button and there is an additional button to reset all sliders for ease of use.
     
     <img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/cb464745-ca58-46d9-b109-a5c031d6246d">
3. VCF Data Filter:
   - This includes a slider for allele frequency (AF) since that was the only desired metric for filtering.
   - The VCF Linking needs to be selected as Yes to apply this filter, else an error is thrown.
     
     <img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/801ce5cb-39cd-41db-8caf-0203dc7e0600">
4. Advanced Data Filter:
   - This section allows for advanced filtering such as performing group-bys and aggregate functions on numerical columns.
   - The default is None.
     
     <img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/0f9fcfed-e14d-46c7-8c73-66f528f3a337">
5. Displayed table:
   - The table which is obtained as the output of the filters can be viewed easily since horizontal and vertical scrolling is enabled.
   - Additionally the table can be downloaded as a csv file if required.
     
     <img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/5ff84013-203f-4ee3-8071-d1d582dfadc5">
     
 ## Graphs Tab
<img width="947" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/45512d30-af18-4f41-a888-4394e9dd2586">
 
1. Visualising count of a genotype of interest
   - This is a bar graph which displays a genotype of interest (Homozygous Ref/Homozygous Alt/Heterozygous) based on a particular Scaffold ID sorted by location. The graphs are generated using [Google Charts.](https://developers.google.com/chart)
   - This can be useful to study the distribution of potential Scaffold ID in corals that show higher survival rate.
   - The images can be downloaded if required, or viewed in a new browser tab
2. Visualising ecological volume across years
   - This is a simple line graph to study the growth of a coral of interest (using unique Tag IDs) across the 4 years of data collected. Ecological volume is calculated using the length/width/height of a coral.
   - This graph is useful to study how the coral colonies are doing in a location and if any natural factors may have affected this.
   - Again the image can be downloaded if required, or viewed in a new tab.

## Media Tab

<img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/fe6694bc-62fc-467b-b55a-93eea58aee4e">

- This tab hosts images taken by the [BU Marine Program](https://bumarine.smugmug.com/) during their field work but the Coral Database website hosts images specific to only coral species.
- Each image has a description which pops up by hovering ones cursor over it, since there is a Javascript tooltips function which extracts the image description and displays that dynamically for each image.
- The headers link out to the particular species BU Marine folder which hosts more images from the same species and can be downloaded through their website if required.
- Additionally each image can be viewed in detail by clicking on it which is possible due to [Lightbox](https://github.com/lokesh/lightbox2) Javascript library.
  
  <img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/d4123a88-2f91-4b86-ada3-1cb6efcb7e85">

 ## Help Tab
 <img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/f8bf23f1-3ab6-4360-87b5-1062d6aa4fbd">
 
 - This tab hosts a guide and in depth FAQs on each section and input required so that people with a non-scientific and non-Bioinformatic background can easily use the site as well.
 - When a header is clicked in other tabs, the user is re-directed to the help tab, where the corresponding section is centered and highlighted for ease of use.
<img width="650" alt="image" src="https://github.com/saumyapo/Coral-Database/assets/144373823/ba429411-42d4-4a8c-82c9-1656a7f90f4f">








