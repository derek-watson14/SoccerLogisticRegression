from imports import *

all_predictors = ["Matchday", "Position", "Wins", "Draws", "Losses", "Goals For", "Goals Against", "Goal Differential",
                  "Points", "Appearances", "Points Per Week", "Stadium Size_Average", "Stadium Size_Large"]

def forward_stepwise(all_predictors, train, test):
    # Implementation of forward stepwise selection
    # Run time = n^2
    models_by_step = []
    best_score = 0
    best_p = ""
    best_model = []
    saved_llf = float('-inf')
    for q in range(len(all_predictors)):
        for p in all_predictors:
            preds = best_model.copy()
            preds.append(p)
            model = OrderedModel(train['Fate'], 
                             train[preds],
                             distr='logit'); 
            result = model.fit(method='powell', disp=0, skip_hessian=True);
            curr_llf = result.llf
            predicted = result.model.predict(result.params, exog=test[preds]);
            pred_choice = predicted.argmax(1)
            score = (test['Fate'].values.codes == pred_choice).mean()
            if score > best_score:
                best_score = score
                best_p = p
                saved_llf = curr_llf

        best_model.append(best_p)
        all_predictors.remove(best_p)
        models_by_step.append((best_p, best_score, best_model.copy(), saved_llf))
        best_score = 0
        best_p = ""
        curr_llf = float('-inf')

    return models_by_step

class Categorizer:
    # Class used to categorize data
    # Creates categories for stadium size and EOS fate
    size_cat = pd.CategoricalDtype(categories=["Small", "Average", "Large"], ordered=True)
    fate_cat = pd.CategoricalDtype(categories=["Relegation", "Lower Mid-Table", "Upper Mid-Table", "Europa/Conference League", "Champions League"],ordered=True)

    def categorize_stadium(self, row):
        cap = row["Stadium Capacity"]
        if cap <= 17500:
            return "Small"
        elif cap > 17500 and cap < 40000:
            return "Average"
        else:
            return "Large"

    def categorize_fate(self, row):
        pos = row["EOS Position"]
        if pos <= 4:
            return "Champions League"
        elif pos >= 5 and pos <= 7:
            return "Europa/Conference League"
        elif pos >= 8 and pos <= 12:
            return "Upper Mid-Table"
        elif pos >= 13 and pos <= 17:
            return "Lower Mid-Table"
        else:
            return "Relegation"

    def categorize_fate_niave(self, row):
        pos = row["Position"]
        if pos <= 4:
            return "Champions League"
        elif pos >= 5 and pos <= 7:
            return "Europa/Conference League"
        elif pos >= 8 and pos <= 12:
            return "Upper Mid-Table"
        elif pos >= 13 and pos <= 17:
            return "Lower Mid-Table"
        else:
            return "Relegation"