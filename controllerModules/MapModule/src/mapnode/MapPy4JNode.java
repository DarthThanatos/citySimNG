package mapnode;

import com.google.common.eventbus.Subscribe;
import controlnode.DispatchCenter;
import controlnode.Py4JNode;
import model.DependenciesRepresenter;
import model.TutorialHintEvent;
import py4jmediator.MapPresenter;
import py4jmediator.MapResponses.DeleteBuildingResponse;
import py4jmediator.MapResponses.PlaceBuildingResponse;
import py4jmediator.MapResponses.StopProductionResponse;
import py4jmediator.Presenter;

import java.util.Map;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class MapPy4JNode extends Py4JNode implements MapPresenter.OnMapPresenterCalled {
    public Thread resourcesThread;
    public boolean updateResources = true;

    public Buildings buildings;
    public Dwellers dwellers;
    public Resources resources = null;

    public boolean startNewGame = true;

    private final Lock lock = new ReentrantLock();
    private final Condition viewNotInitialized = lock.newCondition();
    private boolean viewInitialized = false;

    public MapPy4JNode(DependenciesRepresenter dependenciesRepresenter, DispatchCenter dispatchCenter, String nodeName){
        super(dependenciesRepresenter, dispatchCenter, nodeName);
        resources = new Resources(dr);
        buildings = new Buildings(dr);
        dwellers = new Dwellers(dr);
    }

    @Override
    public void atStart(){
        MapPresenter mapPresenter = Presenter.getInstance().getMapPresenter();
        mapPresenter.setOnMapPresenterCalled(this);
        mapPresenter.displayMap();

        waitForViewInit();

        if(startNewGame) {
            lock.lock();
            viewInitialized = false;
            lock.unlock();

            startNewGame = false;
            resources = new Resources(dr);
            buildings = new Buildings(dr);
            dwellers = new Dwellers(dr);
            mapPresenter.init(
                    resources.getResources(),
                    buildings.getDomesticBuildings(),
                    buildings.getIndustrialBuildings(),
                    dwellers.getAllDewellers(),
                    dr.getTextureAt(0),
                    dr.getTextureAt(1),
                    dr.getPanelTexture(),
                    dr.getMp3(),
                    resources.getActualResourcesValues(),
                    resources.getActualResourcesIncomes(),
                    resources.getActualResourcesConsumption(),
                    resources.getResourcesBalance(),
                    dwellers.getAvailableDwellers());

            waitForViewInit();

        }
        else{
            mapPresenter.resumeGame();
        }

        updateResources = true;
        resourcesThread = new Thread() {
            public void run() {
                while (updateResources) {
                    resources.calculateCurrentCycle(dwellers, buildings);
                    mapPresenter.updateValuesForCycle(
                            resources.getActualResourcesValues(),
                            resources.getActualResourcesIncomes(),
                            resources.getActualResourcesConsumption(),
                            resources.getResourcesBalance(),
                            dwellers.getNeededDwellers(),
                            dwellers.getAvailableDwellers());
                    try {
                        Thread.sleep(3000);
                    } catch (Exception e) {

                    }
                }
            }
        };
        resourcesThread.start();
        registerEvBus();
    }

    @Subscribe
    public void onTutotialHintEvent(TutorialHintEvent tutorialHintEvent){
        //TODO - implementing reaction on tutorialHintEvent receipt
    }

    @Override
    public void onLoop(){

    }

    private void unregisterEvBus(){
        try{
            dispatchCenter.getEventBus().unregister(this);
        }catch(Exception e) {

        }
    }

    private void registerEvBus(){
        try {
            dispatchCenter.getEventBus().register(this);
        }
        catch(Exception e){

        }

    }

    @Override
    public void atUnload(){
        startNewGame = true;
        super.atUnload();
    }

    @Override
    public void atExit(){
        unregisterEvBus();
        resourcesThread.interrupt();
        updateResources = false;
        Presenter.getInstance().getMapPresenter().setOnMapPresenterCalled(null);
    }

    @Override
    public void onGoToMenu(){
        lock.lock();
        viewInitialized = false;
        lock.unlock();
        moveTo("GameMenuNode");
    }


    @Override
    public PlaceBuildingResponse onPlaceBuilding(String buildingName, String buildingId){
        return buildings.placeBuilding(buildingName, buildingId, resources, dwellers);
    }

    @Override
    public boolean onCheckIfCanAffordOnBuilding(String buildingName){
        return buildings.canAffordOnBuilding(buildingName, resources.getActualResourcesValues());
    }

    @Override
    public DeleteBuildingResponse onDeleteBuilding(String buildingId){
        return buildings.deleteBuilding(buildingId, resources, dwellers);
    }

    @Override
    public StopProductionResponse onStopProduction(String buildingId){
        return buildings.stopProduction(buildingId, resources, dwellers);
    }

    @Override
    public Integer onGetWorkingDwellers(String buildingId){
        return buildings.getWorkingDwellers(buildingId);
    }

    @Override
    public void onViewInitialized(){
        lock.lock();
        viewInitialized = true;
        viewNotInitialized.signal();
        lock.unlock();
    }

    private void waitForViewInit(){
        lock.lock();
        while(!viewInitialized){
            try{
                viewNotInitialized.await();
            } catch (InterruptedException e){
                System.out.println(e.getMessage());
            }
        }
        lock.unlock();
    }
}
