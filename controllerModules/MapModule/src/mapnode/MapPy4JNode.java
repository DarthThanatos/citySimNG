package mapnode;

import com.google.common.eventbus.Subscribe;
import controlnode.DispatchCenter;
import controlnode.Py4JNode;
import entities.Building;
import entities.Dweller;
import entities.Entity;
import entities.Resource;
import model.DependenciesRepresenter;
import model.TutorialHintEvent;
import py4jmediator.MapPresenter;
import py4jmediator.MapResponses.DeleteBuildingResponse;
import py4jmediator.MapResponses.EndGameResponse;
import py4jmediator.MapResponses.PlaceBuildingResponse;
import py4jmediator.MapResponses.StopProductionResponse;
import py4jmediator.Presenter;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
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

    private MapPresenter mapPresenter;

    public MapPy4JNode(DependenciesRepresenter dependenciesRepresenter, DispatchCenter dispatchCenter, String nodeName){
        super(dependenciesRepresenter, dispatchCenter, nodeName);
        resources = new Resources(dr);
        buildings = new Buildings(dr);
        dwellers = new Dwellers(dr);
    }

    @Override
    public void atStart(){
        mapPresenter = Presenter.getInstance().getMapPresenter();
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
                    new ArrayList<>(resources.getResources().values()),
                    new ArrayList<>(buildings.getDomesticBuildings().values()),
                    new ArrayList<>(buildings.getIndustrialBuildings().values()),
                    new ArrayList<>(dwellers.getAllDewellers().values()),
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

        startResourcesThread();
        registerEvBus();
    }

    private void startResourcesThread(){
        updateResources = true;
        resourcesThread = new Thread(() -> {
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
        });
        resourcesThread.start();

    }

    @Subscribe
    public void onTutotialHintEvent(TutorialHintEvent tutorialHintEvent){
        mapPresenter.sendTutorialHints(tutorialHintEvent.getHints());
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

    @Override
    public EndGameResponse onEndGame(){
        resourcesThread.interrupt();
        updateResources = false;
        startNewGame = true;

        Map<String, Integer> domesticBuildingsSummary = new HashMap<>();
        Map<String, Integer> industrialBuildingsSummary = new HashMap<>();
        Map<String, Integer> dwellersSummary = new HashMap<>();

        for(Building building: buildings.getDomesticBuildings().values())
            domesticBuildingsSummary.put(building.getName(), 0);

        for(Building building: buildings.getIndustrialBuildings().values())
            industrialBuildingsSummary.put(building.getName(), 0);

        for(Dweller dweller: dwellers.getAllDewellers().values())
            dwellersSummary.put(dweller.getName(), 0);
        System.out.println(dwellersSummary);

        for(Building building: buildings.getPlayerDomesticBuildings().values())
            domesticBuildingsSummary.put(building.getName(), domesticBuildingsSummary.get(building.getName()) + 1);

        for(Building building: buildings.getPlayerIndustrialBuildings().values()) {
            industrialBuildingsSummary.put(building.getName(), industrialBuildingsSummary.get(building.getName()) + 1);
            dwellersSummary.put(building.getDwellersName(),
                    dwellersSummary.get(building.getDwellersName()) +
                            building.getWorkingDwellers());
        }

        int score = 0;

        score += calculateScore(resources.getActualResourcesValues(),
                resources.getResources(), Resources.getScoreMultiplier());
        score += calculateScore(domesticBuildingsSummary,
                buildings.getDomesticBuildings(), Buildings.getScoreMultiplier());
        score += calculateScore(industrialBuildingsSummary,
                buildings.getIndustrialBuildings(), Buildings.getScoreMultiplier());
        score += calculateScore(dwellersSummary,
                dwellers.getAllDewellers(), Dwellers.getScoreMultiplier());

        return new EndGameResponse(
                resources.getActualResourcesValues(),
                domesticBuildingsSummary,
                industrialBuildingsSummary,
                dwellersSummary,
                score);
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


    public int calculateScore(Map<String, Integer> entitySummary,
                              Map<String, ? extends Entity> entities,
                              int basicMultiplier){
        int score = 0;
        int multiplier;
        Entity pred;

        for(Entity entity: entities.values()){
            multiplier = basicMultiplier;
            pred = entities.get(entity.getPredecessor());
            while(pred != null){
                multiplier += basicMultiplier;
                pred = entities.get(pred.getPredecessor());
            }
            score += multiplier * entitySummary.get(entity.getName());
        }

        return score;
    }
}
