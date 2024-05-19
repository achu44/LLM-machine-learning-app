# TASK

Created a data science application that leverages a Large Language Model (LLM) (OpenAI GPT 3.5 API or higher) to perform typical data science tasks using natural langauge queries. 

The application supports the following:

1. Data Exploration and Visualization
2. Data Preprocessing and Feature Engineering
3. Training Machine Learning Models
4. Model Evaluation and Interpretation

# INSTRUCTIONS FOR USING APP

Please add an OpenAI API Key to the secrets.toml file in app/.streamlit for the application to be able to properly run and work.

The application is executable by running `docker-compose build && docker-compose up` from the root directory of the repository.

A typical process for using the app is:
1. Enter natural language query, which prompts GPT to generate code
2. Type into input box "run code:" and then copy entire contents of code into input box and Enter
3. If there's an error, input "I got this error " + copy the error message into the input box and Enter
4. Repeat until you see messaage "Code executed successfully."

Usually if you follow this process, most of the time, GPT is able to resolve issues on its own.

On the training tab, the code is set up so that the user should type "train model:" when generating the direct training code; this part pulls in the model name from the text box at the top of the page.

If 'fit' is in the entered code, the application tries to save the nmodel to st.session_state.

If I had more time, I would modularize the code more and reduce code redundancy across app.py and the pages.

I generated an architecture diagram using GPT but it was in ASCII characters and wasn't super informative so I didn't include it.


A sample data set can be found in the included file named “AnalysisData.csv”.
In this file, you will find data for 6098 wells from the Midland Basin,
with 1 row per well. The columns in the dataset are as follows:

| Column Name | Column Units | Description Column | Group |
| ------------|--------------|---------------------|-------|
|SurfaceLongitude|Decimal Degrees| The Longitude of the surface hole location|Location|
|SurfaceLatitude|Decimal Degrees| The Latitude of the surface hole location|Location|
|BottomHoleLongitude|Decimal Degrees| The Longitude of the bottom hole location|Location|
|BottomHoleLatitude|Decimal Degrees| The Latitude of the bottom hole location|Location|
| Operator | None (string) | Company that operates the well | Completion |
|CompletionDate | None (date) |Date in which the well was completed| Completion|
|Reservoir | None (string) | Geologic formation that the well is targeting |Geology|
|LateralLength_FT | Feet | Completed length of the horizontal well |Completion|
|ProppantIntensity_LBSPerFT | Pounds / Feet | Amount of proppant (frac sand) per lateral foot used to complete the well | Completion
|FluidIntensity_BBLPerFT | Barrels / Feet | Amount of fluid per lateral foot used to complete the well | Completion
|HzDistanceToNearestOffsetAtDrill | Feet | Horizontal distance to the nearest offset well - measured at the time the well was completed | Well spacing
|HzDistanceToNearestOffsetCurrent | Feet | Horizontal distance to the nearest offset well - measured at current time | Well spacing
|VtDistanceToNearestOffsetCurrent | Feet | Vertical distance to the nearest offset well - measured at the time the well was completed | Well spacing
|VtDistanceToNearestOffsetAtDrill | Feet | Vertical distance to the nearest offset well - measured at current time | Well spacing
|WellDepth                       | Feet | Depth of the horizontal well | Geology
|ReservoirThickness | Feet | Thickness of the targeted reservoir | Geology
|OilInPlace | Million barrels of oil / square mile | Amount of oil in place for the target reservoir | Geology
|Porosity | Percent | Porosity of the target reservoir | Geology
|ReservoirPressure | PSI |Pressure of the target reservoir | Geology
|WaterSaturation | Percent | % saturation of water in the target reservoir fluid | Geology
|StructureDerivative | Percent | % change in depth of the target formation - proxy for geologic faults | Geology
|TotalOrganicCarbon | Percent | % of total organic carbon of the target formation | Geology
|ClayVolume | Percent | % clay of the target reservoir | Geology
|CarbonateVolume | Percent | % carbonate of the target reservoir | Geology
|Maturity |Percent |Maturity of the target reservoir |Geology|
|TotalWellCost_USDMM |Millions of dollars |Total cost of the horizontal well |Completion|
|CumOil12Month |Barrels of oil| Amount of oil produced in the first 12 months of production |Production
|rowID |None (ID) |unique identifier for each well| ID
