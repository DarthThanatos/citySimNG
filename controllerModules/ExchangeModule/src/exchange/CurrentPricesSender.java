package exchange;

import com.google.common.eventbus.EventBus;
import exchangenode.ExchangeNode;
import io.reactivex.Observable;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import model.ExchangeCurrentPricesEvent;
import utils.DisposingUtils;

import java.util.concurrent.TimeUnit;

public class CurrentPricesSender {

    private Disposable curPricesSendingDisposable;
    private EventBus eventBus;
    private ExchangeNode exchangeNode;

    public CurrentPricesSender(ExchangeNode exchangeNode, EventBus eventBus){
        this.eventBus  = eventBus;
        this.exchangeNode = exchangeNode;
        startSending();

    }

    private void startSending(){
        //TODO - more sophisticated algorithm of calculating when prices should be sent needed
        curPricesSendingDisposable = Observable.interval(5, TimeUnit.SECONDS)
                .subscribeOn(Schedulers.newThread())
                .forEachWhile(this::notInterrupted, Throwable::printStackTrace);
    }

    private boolean notInterrupted(Long aLong) {
        System.out.println("Sending current prices to game menu.");
        eventBus.post(new ExchangeCurrentPricesEvent(exchangeNode.getCurrentPrices()));
        return true;
    }

    public void atUnload(){
        System.out.println("Stopping sending prices.");
        DisposingUtils.dispose(curPricesSendingDisposable);
    }
}
