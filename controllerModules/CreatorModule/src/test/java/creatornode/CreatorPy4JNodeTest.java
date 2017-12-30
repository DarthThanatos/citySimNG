package creatornode;

import constants.Consts;
import controlnode.DispatchCenter;
import entities.Building;
import entities.Dweller;
import entities.Resource;
import model.DependenciesRepresenter;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mock;
import py4jmediator.CreatorData;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.logging.Logger;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

public class CreatorPy4JNodeTest {
    private static Logger log = Logger.getLogger(CreatorPy4JNode.class.getName());
    private static final String MP3_MOCKED =  "some.mp3";
    private static final String TEXTURE_ONE_MOCKED = "text_one.jpg";
    private static final String TEXTURE_TWO_MOCKED = "text_two.jpg";
    private static final String PANEL_TEXTURE_MOCKED = "panel_text.jpg";
    private static final String SET_NAME_MOCKED = "set_name";

    @Mock
    private DispatchCenter dispatchCenter;

    @Mock
    private CreatorData creatorData;
    private HashMap<String, DependenciesRepresenter> representers;

    private void mockDispatchCenter(){
        dispatchCenter = mock(DispatchCenter.class);
        when(dispatchCenter.getDispatchData(Consts.LOADER_MODULE, Consts.DEPENDENCIES_REPRESENTERS)).thenReturn(representers);
    }

    private void mockCreatorData(){
        creatorData = mock(CreatorData.class);
        when(creatorData.getMp3()).thenReturn(MP3_MOCKED);
        when(creatorData.getTextureOne()).thenReturn(TEXTURE_ONE_MOCKED);
        when(creatorData.getTextureTwo()).thenReturn(TEXTURE_TWO_MOCKED);
        when(creatorData.getDependenciesSetName()).thenReturn(SET_NAME_MOCKED);
        when(creatorData.getPanelTexture()).thenReturn(PANEL_TEXTURE_MOCKED);

        Resource resource = new Resource();
        Building building = new Building();
        Dweller dweller = new Dweller();
        List<Building> buildingList = new ArrayList(Arrays.asList(building));
        List<Dweller> dwellerList = new ArrayList(Arrays.asList(dweller));
        List<Resource> resourceList = new ArrayList(Arrays.asList(resource));

        when(creatorData.getBuildings()).thenReturn(buildingList);
        when(creatorData.getResources()).thenReturn(resourceList);
        when(creatorData.getDwellers()).thenReturn(dwellerList);
    }

    @Before
    public void init(){
        representers = new HashMap<>();
        mockDispatchCenter();
        mockCreatorData();
    }


    private void testMoonMetaData(DependenciesRepresenter moonDependenciesRepresenter){
        assertEquals(moonDependenciesRepresenter.getTextureAt(0), "Moon\\background\\moon_bg.jpg");
        assertEquals(moonDependenciesRepresenter.getTextureAt(1), "Moon\\background\\moon_bg2.jpg");
        assertEquals(moonDependenciesRepresenter.getMp3(), "TidesMain.mp3");
        assertEquals(moonDependenciesRepresenter.getPanelTexture(), "Moon\\background\\panel.jpg");
    }

    private void testMoonDeps(){
        DependenciesRepresenter moonDependenciesRepresenter = representers.get("Moon");
        assertNotNull(moonDependenciesRepresenter);
        testMoonMetaData(moonDependenciesRepresenter);
        assertEquals(moonDependenciesRepresenter.getBuildingsNames().size(), 16);
        assertEquals(moonDependenciesRepresenter.getResourcesNames().size(),13);
        assertEquals(moonDependenciesRepresenter.getDwellersNames().size(), 4);
    }

    private void testStrongholdMetadata(DependenciesRepresenter strongholdDependenciesRepresenter){

        assertEquals( strongholdDependenciesRepresenter.getTextureAt(0), "Middleages\\background\\meadow1.jpg");
        assertEquals( strongholdDependenciesRepresenter.getTextureAt(1), "Middleages\\background\\meadow2.jpg");
        assertEquals( strongholdDependenciesRepresenter.getMp3(), "TwoMandolins.mp3");
        assertEquals( strongholdDependenciesRepresenter.getPanelTexture(), "Middleages\\background\\drewno.jpg");
    }

    private void testStrongholdDeps(){
        DependenciesRepresenter strongholdDependenciesRepresenter = representers.get("Stronghold");
        assertNotNull(strongholdDependenciesRepresenter);
        testStrongholdMetadata(strongholdDependenciesRepresenter);
        assertEquals(strongholdDependenciesRepresenter.getBuildingsNames().size(), 14);
        assertEquals(strongholdDependenciesRepresenter.getResourcesNames().size(),10);
        assertEquals(strongholdDependenciesRepresenter.getDwellersNames().size(), 4);
    }
    @Test
    public void testDefaultSets(){
        //representers map is filled in the constructor of CreatorNode
        new CreatorPy4JNode(dispatchCenter, "Creator",
                "..\\..\\resources\\sysFiles\\defaultDependencies\\");
        assertEquals(representers.size(), 2);
        testMoonDeps();
        testStrongholdDeps();
    }

    private void testCreatedDRMetadata(DependenciesRepresenter createdDependenciesRepresenter){
        assertEquals(TEXTURE_ONE_MOCKED, createdDependenciesRepresenter.getTextureAt(0));
        assertEquals(TEXTURE_TWO_MOCKED, createdDependenciesRepresenter.getTextureAt(1));
        assertEquals(PANEL_TEXTURE_MOCKED, createdDependenciesRepresenter.getPanelTexture());
        assertEquals(MP3_MOCKED, createdDependenciesRepresenter.getMp3());
    }

    @Test
    public void testCreatorInput(){
        CreatorPy4JNode creatorPy4JNode = new CreatorPy4JNode(dispatchCenter, "Creator", "..\\..\\resources\\sysFiles\\defaultDependencies\\");
        try{
            creatorPy4JNode.onCreateDependencies(creatorData);
        }
        catch(Exception e){
            log.info("Presenter not active");
        }
        DependenciesRepresenter createdDependenciesRepresenter = representers.get(SET_NAME_MOCKED);
        assertNotNull(createdDependenciesRepresenter);
        testCreatedDRMetadata(createdDependenciesRepresenter);
        assertEquals(createdDependenciesRepresenter.getBuildingsNames().size(), 1);
        assertEquals(createdDependenciesRepresenter.getResourcesNames().size(),1);
        assertEquals(createdDependenciesRepresenter.getDwellersNames().size(), 1);
    }

    @Test
    public void testLoaderNode(){
        new CreatorPy4JNode(dispatchCenter, "Creator","..\\..\\resources\\sysFiles\\defaultDependencies\\");
        verify(dispatchCenter, times(1)).getDispatchData("LoaderModule","DependenciesRepresenters");
        LoaderPy4JNode loaderPy4JNode = new LoaderPy4JNode(dispatchCenter, "Loader");
        verify(dispatchCenter, times(1)).getDispatchData("LoaderModule","DependenciesRepresenters");
    }
}