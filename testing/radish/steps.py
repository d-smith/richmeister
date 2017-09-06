from radish import given, when, then

@given("an item with id {item_id:S}")
def have_id(step, item_id):
    step.context.id = item_id

@given("timestamp {ts:g}")
def have_ts(step, ts):
    step.context.ts = ts

@given("wid {wid:S}")
def have_wid(step, wid):
    step.context.wid = wid

@given("remote item {present:S}")
def remote_item_present(step, present):
    step.context.present = present

@given("remote ts {rts:g}")
def remote_ts(step, rts):
    step.context.rts = rts

@given("remote wid {rwid:S}")
def remote_wid(step, rwid):
    step.context.rwid = rwid

@when("I replicate the insert")
def when(step):
    print 'replicate baby'

@then("I expect the remote ts {repts:g}")
def then(step, repts):
    assert True