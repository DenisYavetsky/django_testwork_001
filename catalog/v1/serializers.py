from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from catalog.models import Product, Category, PropertyObject, PropertyValue


class PropsSerializer(ModelSerializer):
    props = serializers.SerializerMethodField()

    def get_props(self, obj):
        props = obj.props.all()
        properties = []
        for prop in props:
            properties.append({
                'id': prop.id,
                'name': prop.name,
                'count': PropertyValue.objects.filter(prop=prop).count(),
            })
        return properties


    class Meta:
        model = Category
        fields = '__all__'


class ProductCreateSerializer(ModelSerializer):
    props = serializers.ListField()

    def validate(self, data):
        """
            json in
            {
                "name": "name",
                "article": "article",
                "category": "category",
                "slug": "slug",
                "props": [
                    {
                        "p_object": "p_object",
                        "value_type": "int",
                        "p_value": "p_value"
                    },
                    {
                        "p_object": "p_object",
                        "value_type": "int",
                        "p_value": "p_value"
                    },
                    {
                        "p_object": "p_object",
                        "value_type": "int",
                        "p_value": "p_value"
                    }
                ]
        """
        try:
            category = Category.objects.get(id=data['category'].id)
            for p in data['props']:
                property_object = PropertyObject.objects.get(id=p['p_object'])
        except Exception as e:
            raise serializers.ValidationError('category or property not found')
        return data

    def create(self, validated_data):
        property_objects = validated_data.pop('props')
        product = Product.objects.create(**validated_data)
        for p in property_objects:
            property_value_data = {
                'prop': PropertyObject.objects.get(id=p['p_object'])
            }
            if p['value_type'] == 'int':
                property_value_data['digit_val'] = p['p_value']
            else:
                property_value_data['str_val'] = p['p_value']
            property_value = PropertyValue.objects.create(**property_value_data)
            property_value.product.add(product)
        self.fields.pop('props')
        return product

    class Meta:
        model = Product
        fields = '__all__'


class ProductReadSerializer(ModelSerializer):
    category = serializers.CharField()
    props = serializers.SerializerMethodField()

    def get_props(self, obj):
        props = obj.category.props.all()
        properties = []
        for prop in props:
            props_values = PropertyValue.objects.get(prop=prop, product=obj)
            properties.append({
                'prop_name': prop.name,
                'str_val': props_values.str_val,
                'digit_val': props_values.digit_val,
                'code_url': props_values.code_url,
            })
        return properties

    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
