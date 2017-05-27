# attribra
NVDA Add-On that adds Braille Attributes capability

This NVDA Add-On gives the possibility to the user to define custom rules to mark text with special fields option with braille dots 7 and 8.
In short you can mark bold, italic, specific foreground or background colors etc. using dots 7 and 8 of your refreshable braille display.

When I tried to switch to NVDA as my former screen reader, I've found that Braille Attributes were missing.
Since I'm a prolificient braille user, I tried to open an issue here:
https://github.com/nvaccess/nvda/issues/3022

Since I didn't like the solution, I started developing this addon. I've been using it for two years without any issue, so I decided to publish it.

Features provided by this addon are **independent** from the Document Formatting option: i.e. you can mark spelling errors without have the option selected on the Document Formatting dialog.

It supports both application-specific or global configuration rules.
In order to edit rules you have to manually edit the attribra.ini configuration file.

Examples of configuration rules are:

```
[winword]
invalid-spelling = 1
```

Braille marking of spelling errors in Word

```
[eclipse]
"background-color" = "rgb(24420045)", "rgb(2550128)"
```

Marks errors and warnings in braille while using the Eclipse IDE.

```
[firefox]
color = "RGB(255,0,0)"
```

Braille marking of red text

```
[global]
bold = 1
```

Marks bold text in all applications excepts firefox, eclipse and winword for which a specific configuration exists

To determine the name and the value of the rules you need, you can use the "debug mode".
To toggle debug mode press **Control+Shift+NVDA+B**
This will log all the information about the text while you move around. Pleas usse this option carefully and only for a short amount of time, for instance when you have already located a text with the pattern you want to be marked.
After that, toggle this option off and review the log from the NVDA tools menu.
Identify the property you want to mark and report it in the attribra configuration file.


##Add-On Shortcuts:
* **NVDA+Control+B**: Open the attribra.ini file with your default INI editor
* **NVDA+Control+Shift+B**: Toggle debug logging on or / off

##Author
Alberto Zanella <lapostadi[myfirstname]#gmail.com>
