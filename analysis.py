import subprocess, os, sys, json, shutil

os.chdir('./src/yolo')

file=sys.argv[1]
filename, ext = os.path.splitext(file)
image_path = f'./runs/detect/{filename}/{file}'
label_path = f'./runs/detect/{filename}/labels/{filename}.txt'

with open('./labels.json','r') as label:
  label_data = json.load(label)

try:
  subprocess.run(f'python detect.py --source ../../images/{file} --conf 0.50 --weights ./runs/best.pt --name {filename} --save-txt',check=True,timeout=20,shell=True)

  shutil.copy(image_path,f'../../images/Detect_{file}')

  coin = []

  if os.path.exists(label_path):
    with open(label_path) as file:
      lines = file.readlines()

      for line in lines:
        coin.append(line[0])
  coinList = list(map(lambda coinID: label_data[coinID],coin))

  resData = {}

  for name in coinList:
    value, country=name.split(" ")
    country = country[:3]
    if resData.get(country):

      if resData[country].get(value):
        resData[country][value] += 1
      else:
        resData[country][value] = 1

    else:
      resData[country] = {value:1}

  print(resData)
    
except:
  raise Exception("Script execution stopped")