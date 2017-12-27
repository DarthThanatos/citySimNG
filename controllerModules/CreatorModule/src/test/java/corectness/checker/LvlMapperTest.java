package corectness.checker;

import constants.Consts;
import controlnode.DispatchCenter;
import creatornode.CreatorPy4JNode;
import model.DependenciesRepresenter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;

import java.util.HashMap;

import static org.junit.Assert.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

public class LvlMapperTest {

    private LvlMapper lvlMapper = new LvlMapper();

    @Mock
    private DispatchCenter dispatchCenter;

    @Before
    public void setUp() throws Exception {
        HashMap<String, DependenciesRepresenter> representers = new HashMap<>();
        dispatchCenter = mock(DispatchCenter.class);
        when(dispatchCenter.getDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS)).thenReturn(representers);
        new CreatorPy4JNode(dispatchCenter, "Creator", "..\\..\\resources\\sysFiles\\defaultDependencies\\");

        DependenciesRepresenter lvlDR = representers.get("Moon");
        lvlMapper.mapLevels(
                lvlDR.getGraphsHolder().getResourcesGraphs(),
                lvlDR.getGraphsHolder().getDwellersGraphs(),
                lvlDR.getGraphsHolder().getBuildingsGraphs()
        );
    }

    @Test
    public void testLvlsExist(){
        assertNotNull(lvlMapper.getBuildingsNodesLevels());
        assertNotNull(lvlMapper.getDwellersNodesLevels());
        assertNotNull(lvlMapper.getResourcesNodesLevels());
    }

    @Test
    public void testDwellersLvls(){
        HashMap<String, Integer> dwellersLvls = lvlMapper.getDwellersNodesLevels();
    }


    @Test
    public void testBuildingsLvls(){
        HashMap<String, Integer> buildingsLvls = lvlMapper.getBuildingsNodesLevels();

    }


    @Test
    public void testResourcesLvls(){
        HashMap<String, Integer> resourcesLvls = lvlMapper.getResourcesNodesLevels();
    }
}