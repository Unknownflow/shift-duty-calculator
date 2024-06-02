from datetime import datetime, timedelta
import csv

SCORES_LIST_CALC = {
  "2100-2130":	0.5,
  "2130-2200":	0.5,
  "2200-2230":	0.5,
  "2230-2300":	0.5,
  "2300-2330":	0.5,
  "2330-0000":	0.5,
  "0000-0030":	1,
  "0030-0100":	1,
  "0100-0130":	1,
  "0130-0200":	1,
  "0200-0230":	2,
  "0230-0300":	2,
  "0300-0330":	2.5,
  "0330-0400":	2.5,
  "0400-0430":	2.5,
  "0430-0500":	2.5,
  "0500-0530":	1.5,
  "0530-0600":	1.5,
  "0600-0630":	0.1,
  "0630-0700":	0.1,
}

scores_list_date = {}

with open("time.csv", newline="", encoding='utf-8-sig') as csvfile:
  reader = csv.reader(csvfile)
  curr_date = ""
  for row in reader:
    print(row)
    if row[0].isnumeric(): 
      # new date then add a new dict inside main dict
      curr_date = row[0]
      scores_list_date[curr_date] = {}
    else:
      person_name = row[0]

      # first will store the score, second will store the date
      scores_list_date[curr_date][person_name] = [0, ""]
      scores_list_date[curr_date][person_name][0] = 0

      # no night duty
      if row[1] == "":
        continue
      else:
        # returns start and end time for each person
        person_time_range = row[1].split("\n")
        
        for i in range(len(person_time_range)):
          # returns [start_time, end_time]
          print(person_time_range[i])
          time_range_text = person_time_range[i].split("-")

          # if start time before midnight
          if time_range_text[0][0] == "2":
            start_time = datetime.strptime("01/01/23 " + time_range_text[0], "%d/%m/%y %H%M")
          else:
            start_time = datetime.strptime("02/01/23 " + time_range_text[0], "%d/%m/%y %H%M")

          # if end time before midnight
          if time_range_text[1][0] == "2":
            end_time = datetime.strptime("01/01/23 " + time_range_text[1], "%d/%m/%y %H%M")
          else:
            end_time = datetime.strptime("02/01/23 " + time_range_text[1], "%d/%m/%y %H%M")

          score = 0

          # score calc
          while start_time != end_time:
            initial_start_time_rep = start_time.strftime("%H%M")
            start_time = start_time + timedelta(minutes=30)

            final_start_time_rep = start_time.strftime("%H%M")
            time_range = initial_start_time_rep + "-" + final_start_time_rep

            # add to total score
            score = score + SCORES_LIST_CALC[time_range]

          scores_list_date[curr_date][person_name][0] = round(scores_list_date[curr_date][person_name][0] + score, 3)
          # print(person_time_range[i])
          if scores_list_date[curr_date][person_name][1] == "":
            scores_list_date[curr_date][person_name][1] = person_time_range[i]
          else:
            # this makes sure that if there are 2 night duty timing, data will be wrapped in the same excel cell.
            scores_list_date[curr_date][person_name][1] = '"' + scores_list_date[curr_date][person_name][1] + '\n' + person_time_range[i] + '"'


with open("result.csv", "w") as writefile:
  for date_key in scores_list_date.keys():
    writefile.write(date_key + "\n")
    for name_key in scores_list_date[date_key].keys():
      # if person cannot be found
      if name_key not in scores_list_date[curr_date]:
        continue

      # data in the format: name, night duty timing, night duty score
      writefile.write(name_key + "," + scores_list_date[curr_date][name_key][1] + "," + str(scores_list_date[curr_date][name_key][0]) + "\n")
