'''
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
'''

from user import User
from pathlib import Path
import json

alle_user = []

BASE_DIR = Path(__file__).resolve().parent
json_file = BASE_DIR / "data" / "userdata.json"

with json_file.open("r", encoding="utf-8") as file:
    json_data = json.load(file)
    for obj in json_data:
        user_obj = User.from_dict(obj)
        alle_user.append(user_obj)

print(alle_user)

output_dir = BASE_DIR / "output"
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "new_data.json"

alle_user_as_dicts = [user.to_dict() for user in alle_user]

with output_file.open("w", encoding="utf-8") as file:
    json.dump(alle_user_as_dicts, file, indent=4, ensure_ascii=False)


'''
def register(request, template_name='meine_app/register.html', next_page_name=None):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if next_page_name is None:
                next_page = '/'
            else:
                next_page = reverse(next_page_name)
            return HttpResponseRedirect(next_page)
    else:
        form = UserCreationForm()
    return render(request, template_name, {'form': form})
'''