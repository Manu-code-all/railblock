# Test checklist

Mark PASS / FAIL. Note the bug number for any FAIL.

## Setup
- [ ] App starts with `streamlit run app.py`
- [ ] Opens in the browser without errors
- [ ] Works on a laptop that is not Manu's

## Departments
- [ ] Can pick Engineering / S&T / Traction
- [ ] Can submit a request with all fields
- [ ] The new request appears in the list
- [ ] It is still there after reloading the page
- [ ] Can withdraw a request
- [ ] Cannot submit an empty form

## Controller
- [ ] Sees requests from all three departments
- [ ] Solve produces a plan
- [ ] Says "proven optimal"
- [ ] Gantt chart draws correctly
- [ ] Priority slider changes the plan
- [ ] Rule violations shows 0

## Explanation
- [ ] Can pick any block and see why it is there
- [ ] The reasoning matches what is on the chart
- [ ] Windows considered list looks right

## Conflict
- [ ] The overloaded corridor reports a conflict
- [ ] It names the specific requests
- [ ] The arithmetic in the message is correct
- [ ] Deferring one request makes it solvable

## Block orders
- [ ] Can publish a plan
- [ ] Published plan is visible to departments
- [ ] Export downloads a file
- [ ] The file opens and contents are right

## Activity log
- [ ] Submissions appear
- [ ] Publishing appears
- [ ] Times are correct

## Robustness
- [ ] Duration longer than any window is handled
- [ ] Deadline in the past is handled
- [ ] Zero or negative duration is rejected
- [ ] Very long text does not break the layout
- [ ] Solving twice quickly does not break it
- [ ] Usable at a small window size
