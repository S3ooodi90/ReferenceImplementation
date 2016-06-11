** Data Model Generator ** 
*aka. Data Translator*

See README_polymer.md for details about the infrastructure.
This command serves the app at `http://localhost:8080` and provides basic URL
routing for the app:

    polymer serve


This UI connects to the DMGEN via a REST API.

It controls how CSV data files can be used to drive model development and then translate the CSV into a compliant XML document on a per row basis. 

**STEPS**

    0. Select the file and the type of record separator (comma, semicolon, pipe)
    1. Load the CSV file.
    2. Read the first 10 records if more than 10, otherwise read them all.
    3. Confirm the total number of records and columns with the user. 
    4. For each column attempt to guess the datatype.
    5. Ask the user to confirm/select the correct datatype for each column. 
        a. Is it a string?
            - is it restricted to a set of choices?
            - is it restricted to a regex pattern?
            - does it have a min/max length?

        b. Is it a number?
            - is it integers only?
            - does it have min/max values? are they inclusive/exclusive?
            - are the number of digits limited?
            - if float are decimal positions limited?

        c. Are any two/three columns used together as a rate, proportion or ratio?
            - Select: numerator, denominator, result value

        d. Do you have a URL that points to a definition of this data column?

    6. Offer to allow user to change the column header. Use the header to create the 'label' for each RMC.
        a. In a more advanced version prompt the user for data provenance model (Subject, Provider, Audit, etc.). 
    7. Ask user for a model 'title', 'description', 'copyright', etc. select: 'author' & 'contributors'.
    8. Create the model package.
    9. Generate an XML file for each record in the CSV. 

