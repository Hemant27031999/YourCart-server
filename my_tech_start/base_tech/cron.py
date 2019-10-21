from django.utils import timezone
import datetime
import requests
from .models import Subscribed_Orders


def place_subscribed_order():
    now = timezone.now()
    sorders = Subscribed_Orders.objects.filter(
        delivery_month=now.month(),
        delivery_time__gte=now.time(),
        delivery_time__lte=now + datetime.timedelta(minutes=30)
    )
    strdate = str(now.date())
    strdate = " "+strdate+" "
    strmonth = str(now.month())
    strmonth = " " + strmonth + " "
    sorders_unique = sorders.values("sorder_id").distinct()
    print(sorders_unique)
    l1 = sorders_unique.count()
    for u in range(l1):
        print(sorders_unique[u]['sorder_id'])
        orders = Subscribed_Orders.objects.filter(sorder_id=sorders_unique[u]['sorder_id'])
        items = []
        quantities = []
        l = orders.count()
        if l>0:
            if orders[0].delivery_dates.find(strdate) != -1 and orders[0].delivery_months.find(strmonth) != -1:
                print(orders)
                print(l)
                for i in range(l):
                    print(orders[i].product_id)
                    items.append(orders[i].product_id.product_id)
                    quantities.append(orders[i].quantity)
                #    post_data.append(('items',order.product_id.product_id))
                #    post_data.append(('quantities',order.quantity))
                #    if line[0] in years_dict:
                #        # append the new number to the existing array at this slot
                #        post_data['items'].append(order.product_id.product_id)
                #    else:
                #        # create a new array in this slot
                #        post_data['items'] = [order.quantity]
                post_data = {
                    'phone_no': orders[0].customer_phone.phone_no,
                    'vendor_phone': orders[0].vendor_phone.phone_no,
                    'address': orders[0].address,
                    'items': items,
                    'quantities': quantities,
                    'cust_lat': orders[0].cust_lat,
                    'cust_long': orders[0].cust_long
                }
                print(post_data)
                print(orders[0].sorder_id)
                #    result = urllib.request.urlopen('http://127.0.0.1:8000/place_order/', urllib.parse.urlencode(post_data).encode('utf-8'))
                #    content = result.read()
                #    print(content)
                r = requests.post(url='http://127.0.0.1:8000/place_order/', data=post_data)