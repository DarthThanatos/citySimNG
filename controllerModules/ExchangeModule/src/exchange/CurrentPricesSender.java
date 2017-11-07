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
        curPricesSendingDisposable = Observable.timer(5, TimeUnit.SECONDS)
                .subscribeOn(Schedulers.newThread())
                .subscribe(this::notInterrupted, Throwable::printStackTrace, this::sendPeriodically);
    }

    private boolean notInterrupted(Long aLong) {
        eventBus.post(new ExchangeCurrentPricesEvent(exchangeNode.getCurrentPrices()));
        return true;
    }

    private void sendPeriodically(){
        curPricesSendingDisposable = Observable.interval(2, TimeUnit.MINUTES)
                .subscribeOn(Schedulers.newThread())
                .forEachWhile(this::notInterrupted, Throwable::printStackTrace);
    }

    public void atUnload(){
        DisposingUtils.dispose(curPricesSendingDisposable);
    }
}
