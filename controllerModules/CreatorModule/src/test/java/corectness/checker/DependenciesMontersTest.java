package corectness.checker;

import constants.Consts;
import creatornode.CreatorPy4JNode;
import dependencies.graph.monter.BuildingsMonter;
import dependencies.graph.monter.DwellersMonter;
import dependencies.graph.monter.ResourcesMonter;
import model.DependenciesRepresenter;
import org.json.JSONArray;
import org.junit.Test;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.fail;

public class DependenciesMontersTest {

    private static final String CYCLES_DETECTED_EXPECTED_ERROR_MSG = "Cycle detected when considering Resource\nName";
    private static final String DWELLER_CROSS_DETECTED_EXPECTED_ERROR_MSG = "Dweller Dweller cannot consume Resource1 since Resource1 has bigger lvl";
    private static final String BUILDING_CROSS_CONSUME_EXPECTED_ERROR_MSG = "Building Building cannot consume Resource1 since Resource1 has bigger lvl";
    private static final String BUILDING_CROSS_COSTOF_EXPECTED_ERROR_MSG = "Building Building cannot be built out of Resource1 since Resource1 has bigger lvl";
    private static final String BUILDING_CROSS_DWELLER_EXPECTED_ERROR_MSG = "Dweller Dweller1 cannot be in Building since their levels differ";
    private static final String BUILDING_CROSS_PRODUCE_EXPECTED_ERROR_MSG = "Building Building1 cannot produce Resource since Resource has lower level";
    private static final String BUILDING_CROSS_TYPES_EXPECTED_ERROR_MSG = "Building Building1 has type : Industrial when its predecessor Building has type Domestic";


    private static final String ERRONEOUS_FILE_PATH_PREFIX = "src\\test\\resources\\";
    @Test
    public void testCyclicChecker(){
        JSONArray resourcesArray =
                CreatorPy4JNode
                    .jsonDepsArrayFromFile(ERRONEOUS_FILE_PATH_PREFIX + "cyclic.dep", Consts.RESOURCES);
        try {
            new CyclesChecker(resourcesArray, Consts.RESOURCE_NAME).check();
            fail();
        } catch (CheckException e) {
            assertEquals(CYCLES_DETECTED_EXPECTED_ERROR_MSG, e.getMessage());
        }
    }

    @Test
    public void testDwellersMonter(){
        DependenciesRepresenter dr = new DependenciesRepresenter();
        JSONArray resourcesArray =
                CreatorPy4JNode
                        .jsonDepsArrayFromFile(ERRONEOUS_FILE_PATH_PREFIX + "dweller_cross.dep", Consts.RESOURCES);
        JSONArray dwellersArray =
                CreatorPy4JNode
                        .jsonDepsArrayFromFile(ERRONEOUS_FILE_PATH_PREFIX + "dweller_cross.dep", Consts.DWELLERS);
        try {
            new ResourcesMonter(resourcesArray, dr).mountDependenciesGraph();
            new DwellersMonter(dwellersArray, dr).mountDependendenciesGraph();
            fail();
        } catch (CheckException e) {
            assertEquals(DWELLER_CROSS_DETECTED_EXPECTED_ERROR_MSG, e.getMessage());
        }

    }

    private void testBuildingCrossDetection(String path, String expectedMsg){
        DependenciesRepresenter dr = new DependenciesRepresenter();
        JSONArray resourcesArray =
                CreatorPy4JNode
                        .jsonDepsArrayFromFile(path, Consts.RESOURCES);
        JSONArray dwellersArray =
                CreatorPy4JNode
                        .jsonDepsArrayFromFile(path, Consts.DWELLERS);
        JSONArray buildingsArray =
                CreatorPy4JNode
                        .jsonDepsArrayFromFile(path, Consts.BUILDINGS);

        try {
            new ResourcesMonter(resourcesArray, dr).mountDependenciesGraph();
            new DwellersMonter(dwellersArray, dr).mountDependendenciesGraph();
            new BuildingsMonter(buildingsArray, dr).mountDependenciesGraph();
            fail();
        } catch (CheckException e) {
            assertEquals(expectedMsg, e.getMessage());
        }

    }

    private void testBuildingCrossConsume(){
        testBuildingCrossDetection(
                ERRONEOUS_FILE_PATH_PREFIX + "building_cross_consume.dep",
                BUILDING_CROSS_CONSUME_EXPECTED_ERROR_MSG
        );
    }

    private void testBuildingCrossCostof(){
        testBuildingCrossDetection(
                ERRONEOUS_FILE_PATH_PREFIX + "building_cross_costof.dep",
                BUILDING_CROSS_COSTOF_EXPECTED_ERROR_MSG
        );
    }

    private void testBuildingCrossDweller(){
        testBuildingCrossDetection(
                ERRONEOUS_FILE_PATH_PREFIX + "building_cross_dweller.dep",
                BUILDING_CROSS_DWELLER_EXPECTED_ERROR_MSG
        );
    }

    private void testBuildingCrossProduce(){
        testBuildingCrossDetection(
                ERRONEOUS_FILE_PATH_PREFIX + "building_cross_produce.dep",
                BUILDING_CROSS_PRODUCE_EXPECTED_ERROR_MSG
        );
    }

    private void testBuildingCrossType(){
        testBuildingCrossDetection(
                ERRONEOUS_FILE_PATH_PREFIX + "building_cross_types.dep",
                BUILDING_CROSS_TYPES_EXPECTED_ERROR_MSG
        );
    }

    @Test
    public void testBuildingsChecker(){
        testBuildingCrossConsume();
        testBuildingCrossCostof();
        testBuildingCrossDweller();
        testBuildingCrossProduce();
        testBuildingCrossType();
    }
}


