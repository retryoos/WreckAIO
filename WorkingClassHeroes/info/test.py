import json
'''
data = {}
data['people'] = []
data['people'].append({
    'name': 'Scott',
    'website': 'stackabuse.com',
    'from': 'Nebraska'
})
data['people'].append({
    'name': 'Larry',
    'website': 'google.com',
    'from': 'Michigan'
})
data['people'].append({
    'name': 'Tim',
    'website': 'apple.com',
    'from': 'Alabama'
})
'''
your_json = '[{"name": "product-information", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7IzsjOyM7IzsjOyM7", "path": "/product-information", "description": "Displays information for one or more specified products.", "displayName": "Product Information", "attributes": {}, "resultType": "products", "products": [{"key": "801127com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEyOGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "variants": [{"key": "801128com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEyOGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801128", "variant_key": "801128com_en", "variant_sku": "1010595101170"}}, {"key": "801129com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEyOWNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801129", "variant_key": "801129com_en", "variant_sku": "1010595101180"}}, {"key": "801130com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzMGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801130", "variant_key": "801130com_en", "variant_sku": "1010595101190"}}, {"key": "801131com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzMWNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801131", "variant_key": "801131com_en", "variant_sku": "1010595101200"}}, {"key": "801132com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzMmNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801132", "variant_key": "801132com_en", "variant_sku": "1010595101205"}}, {"key": "801133com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzM2NvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801133", "variant_key": "801133com_en", "variant_sku": "1010595101210"}}, {"key": "801134com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzNGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801134", "variant_key": "801134com_en", "variant_sku": "1010595101220"}}, {"key": "801135com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzNWNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801135", "variant_key": "801135com_en", "variant_sku": "1010595101230"}}, {"key": "801136com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzNmNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801136", "variant_key": "801136com_en", "variant_sku": "1010595101240"}}, {"key": "801137com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzN2NvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801137", "variant_key": "801137com_en", "variant_sku": "1010595101250"}}, {"key": "801138com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzOGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801138", "variant_key": "801138com_en", "variant_sku": "1010595101260"}}, {"key": "801139com_en", "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzOWNvbV9lbjs7Tk9ORTpOT05FOzc0Ow", "attributes": {"variant_id": "801139", "variant_key": "801139com_en", "variant_sku": "1010595101270"}}], "attributes": {"brand": "2137", "brand_name": "Nike SB", "cat": "/4/15", "category": "/Shoes/Sneakers", "color_name": "Black/Dark Grey/Black/White", "deal": "false", "diff_price": "0", "entity_type": "1", "final_price": "114.9500", "gender": "14", "gender_name": "Men", "image": "/9/4/942878.jpg", "is_on_sale": "false", "name": "Shoes - Dunk Mid Pro ISO", "news_rank": "159598", "original_price": "114.9500", "product_id": "801127", "product_key": "801127com_en", "product_sku": "1010595101", "product_special": "", "product_status": "1", "rank": "1", "upsell_ids": "", "url": "skor-dunk-mid-pro-iso-1"}}]}]'
parsed = json.loads(your_json)
print(json.dumps(parsed, indent=4, sort_keys=True))
'''
{
    "productInformation": [
        {
            "attributes": {},
            "description": "Displays information for one or more specified products.",
            "displayName": "Product Information",
            "name": "product-information",
            "path": "/product-information",
            "products": [
                {
                    "attributes": {
                        "brand": "2137",
                        "brand_name": "Nike SB",
                        "cat": "/4/15",
                        "category": "/Shoes/Sneakers",
                        "color_name": "Black/Dark Grey/Black/White",
                        "deal": "false",
                        "diff_price": "0",
                        "entity_type": "1",
                        "final_price": "114.9500",
                        "gender": "14",
                        "gender_name": "Men",
                        "image": "/9/4/942878.jpg",
                        "is_on_sale": "false",
                        "name": "Shoes - Dunk Mid Pro ISO",
                        "news_rank": "159598",
                        "original_price": "114.9500",
                        "product_id": "801127",
                        "product_key": "801127com_en",
                        "product_sku": "1010595101",
                        "product_special": "",
                        "product_status": "1",
                        "rank": "1",
                        "upsell_ids": "",
                        "url": "skor-dunk-mid-pro-iso-1"
                    },
                    "key": "801127com_en",
                    "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEyOGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow",
                    "variants": [
                        {
                            "attributes": {
                                "variant_id": "801128",
                                "variant_key": "801128com_en",
                                "variant_sku": "1010595101170"
                            },
                            "key": "801128com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEyOGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801129",
                                "variant_key": "801129com_en",
                                "variant_sku": "1010595101180"
                            },
                            "key": "801129com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEyOWNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801130",
                                "variant_key": "801130com_en",
                                "variant_sku": "1010595101190"
                            },
                            "key": "801130com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzMGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801131",
                                "variant_key": "801131com_en",
                                "variant_sku": "1010595101200"
                            },
                            "key": "801131com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzMWNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801132",
                                "variant_key": "801132com_en",
                                "variant_sku": "1010595101205"
                            },
                            "key": "801132com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzMmNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801133",
                                "variant_key": "801133com_en",
                                "variant_sku": "1010595101210"
                            },
                            "key": "801133com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzM2NvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801134",
                                "variant_key": "801134com_en",
                                "variant_sku": "1010595101220"
                            },
                            "key": "801134com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzNGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801135",
                                "variant_key": "801135com_en",
                                "variant_sku": "1010595101230"
                            },
                            "key": "801135com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzNWNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801136",
                                "variant_key": "801136com_en",
                                "variant_sku": "1010595101240"
                            },
                            "key": "801136com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzNmNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801137",
                                "variant_key": "801137com_en",
                                "variant_sku": "1010595101250"
                            },
                            "key": "801137com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzN2NvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801138",
                                "variant_key": "801138com_en",
                                "variant_sku": "1010595101260"
                            },
                            "key": "801138com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzOGNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        },
                        {
                            "attributes": {
                                "variant_id": "801139",
                                "variant_key": "801139com_en",
                                "variant_sku": "1010595101270"
                            },
                            "key": "801139com_en",
                            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7cHJvZHVjdF9rZXk7ODAxMTI3Y29tX2VuOzgwMTEzOWNvbV9lbjs7Tk9ORTpOT05FOzc0Ow"
                        }
                    ]
                }
            ],
            "resultType": "products",
            "ticket": "Oy9wcm9kdWN0LWluZm9ybWF0aW9uOyM7IzsjOyM7IzsjOyM7"
        }
    ]
}
'''
