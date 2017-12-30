import entities.Building;
import entities.Dweller;
import junitparams.JUnitParamsRunner;
import junitparams.Parameters;
import mapnode.Dwellers;
import model.DependenciesRepresenter;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

@RunWith(JUnitParamsRunner.class)
public class DwellersUnitTest {

    @Mock
    private static DependenciesRepresenter dependenciesRepresenter;

    private static Map<String, Building> buildingsMap = new HashMap<>();
    private static Map<String, Integer> resourcesMap = new HashMap<>();

    @BeforeClass
    public static void initialize(){
        resourcesMap.put("Grain", 0);
        resourcesMap.put("Wood", 0);
        resourcesMap.put("Gold", 0);
        resourcesMap.put("Bread", 0);
        resourcesMap.put("Flour", 0);
    }

    @Before
    public  void initializeTest() {
        // mock dependency representer
        dependenciesRepresenter = mock(DependenciesRepresenter.class);
        List<Dweller> allDwellers = new ArrayList<>();

        Dweller worker = new Dweller("Worker", "None", "None", "", "");

        allDwellers.add(worker);

        when(dependenciesRepresenter.getModuleData("allDwellers")).thenReturn(allDwellers);

        // create buildings used in tests

        buildingsMap = new HashMap<>();

        Map<String, Integer> fieldProduces = new HashMap<>(resourcesMap);
        fieldProduces.put("Grain", 3);
        Map<String, Integer> fieldConsumes = new HashMap<>(resourcesMap);
        fieldConsumes.put("Wood", 3);
        Map<String, Integer> fieldResourcesCost = new HashMap<>(resourcesMap);
        fieldResourcesCost.put("Wood", 10);
        Building field = new Building("Field", "None", "None", 7, fieldProduces,
                fieldConsumes, fieldResourcesCost, "", "Industrial", "", "Worker");
        buildingsMap.put(field.getName(), field);

        Map<String, Integer> lumberMillProduces = new HashMap<>(resourcesMap);
        lumberMillProduces.put("Gold", 1);
        Map<String, Integer> lumberMillConsumes = new HashMap<>(resourcesMap);
        lumberMillConsumes.put("Bread", 1);
        Map<String, Integer> lumberMillResourcesCost = new HashMap<>(resourcesMap);
        lumberMillResourcesCost.put("Wood", 15);

        Building lumberMill = new Building("LumberMill", "None", "None", 3, lumberMillProduces,
                lumberMillConsumes, lumberMillResourcesCost, "", "Industrial", "", "Worker");
        buildingsMap.put(lumberMill.getName(), lumberMill);
    }

    @Test
    @Parameters({"Field, 0, 5, 5, false",
                 "Field, 2, 5, 7, true",
                 "LumberMill, 1, 2, 3, true",
                 "LumberMill, 3, 0, 3, true"})
    public void updateDwellersWorkingInBuildingTest(String buildingName, int numOfDwellersWorkingInBuilding,
                                                    int expectedNumOfWorkingDwellers,
                                                    Integer expectedNumOfDwellersWorkingInBuilding,
                                                    boolean isFullyOccupied){
        // Given
        Dwellers dwellers = new Dwellers(dependenciesRepresenter);
        Map<String, Building> notFullyOccupiedBuildings = new HashMap<>();
        Building building = buildingsMap.get(buildingName);
        building.setWorkingDwellers(numOfDwellersWorkingInBuilding);

        // When
        dwellers.updateDwellersWorkingInBuilding(building, notFullyOccupiedBuildings);

        // Then
        assertEquals(expectedNumOfWorkingDwellers, dwellers.getWorkingDwellers());
        assertEquals(expectedNumOfDwellersWorkingInBuilding, building.getWorkingDwellers());
        if(!isFullyOccupied)
            assertTrue(notFullyOccupiedBuildings.containsKey(building.getId()));
    }
}