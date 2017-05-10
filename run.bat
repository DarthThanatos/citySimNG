call gradle -q clean
call gradle build
start /B java ^
-cp CreatorModule\bin;^
SystemMainController\bin;^
SkeletonModule\bin;^
ExchangeModule\bin;^
MapModule\bin;^
MenuModule\bin;^
RankingModule\bin;^
TutorialModule\bin;^
lib/json.jar^
 controlswitcher.ControlSwitcher > javaLog.txt
python citySimNGView/Mediator.py