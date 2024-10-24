
#pragma once

#include <vector>

#include "BroadcasterObserver.h"

namespace Kernel
{
    // BroadcasterImpl provides the basic functions for an IEventBroadcaster.
    // By using a template, we can reuse the code for the different kinds of broadcasters
    // while keeping the types unique.
    template<class Observer, class Entity, class Trigger, class TriggerFactory>
    class BroadcasterImpl : IEventBroadcaster<Observer,Entity,Trigger>
    {
    public:
        BroadcasterImpl();
        ~BroadcasterImpl();

        // ISupports
        virtual Kernel::QueryResult QueryInterface(Kernel::iid_t iid, void **ppvObject) override { return Kernel::e_NOINTERFACE; }
        virtual int32_t AddRef() { return 1; }
        virtual int32_t Release() { return 1; }

        // IEventBroadcaster
        virtual void RegisterObserver(   Observer* pObserver, const Trigger& trigger );
        virtual void UnregisterObserver( Observer* pObserver, const Trigger& trigger );
        virtual void TriggerObservers(   Entity*   pEntity,   const Trigger& trigger );
        virtual uint64_t GetNumTriggeredEvents();
        virtual uint64_t GetNumObservedEvents();

        void DisposeOfUnregisteredObservers();

    private:
        std::vector< std::vector<Observer*> > observers;
        std::vector< std::vector<Observer*> > disposed_observers;
        uint64_t num_triggered_events;
        uint64_t num_observed_events;
    };

    class EventTriggerCoordinatorFactory;
    class EventTriggerNodeFactory;
    class EventTriggerFactory;

    class CoordinatorEventBroadcaster : public BroadcasterImpl< ICoordinatorEventObserver,
                                                                IEventCoordinatorEventContext,
                                                                EventTriggerCoordinator,
                                                                EventTriggerCoordinatorFactory>
    {
    };

    class NodeEventBroadcaster : public BroadcasterImpl< INodeEventObserver,
                                                         INodeEventContext,
                                                         EventTriggerNode,
                                                         EventTriggerNodeFactory>
    {
    };

    class IndividualEventBroadcaster : public BroadcasterImpl< IIndividualEventObserver,
                                                               IIndividualHumanEventContext,
                                                               EventTrigger,
                                                               EventTriggerFactory>
    {
    };
}
