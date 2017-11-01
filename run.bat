cd controllerModules
call gradle -q clean
call gradle build
cd ..
start /B java ^
-cp controllerModules\CreatorModule\bin;^
controllerModules\SkeletonModule\bin;^
controllerModules\ExchangeModule\bin;^
controllerModules\MapModule\bin;^
controllerModules\MenuModule\bin;^
controllerModules\TutorialModule\bin;^
controllerModules\SkeletonModule\lib\json.jar;^
controllerModules\SkeletonModule\lib\py4j.jar;^
controllerModules\SkeletonModule\lib\jgrapht-core-1.0.1.jar;^
controllerModules\SkeletonModule\lib\guava.jar;^
controllerModules\SkeletonModule\lib\reactive-streams.jar;^
controllerModules\SkeletonModule\lib\rxjava.jar^
 controlswitcher.ControlSwitcher > javaLog.txt
python citySimNGView/Mediator.py