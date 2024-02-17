from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):    
    invoice = serializers.PrimaryKeyRelatedField(
        queryset=Invoice.objects.all(), required=False
    )
    
    class Meta:
        model = InvoiceDetail
        fields = '__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    details = InvoiceDetailSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = '__all__'

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        invoice = Invoice.objects.create(**validated_data)
        
        for detail_data in details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        return invoice
    
    def to_internal_value(self, data):
        # print(data)        
        return data

    def update(self, instance, validated_data):
        print(validated_data)
        details_data = validated_data.pop('details', [])
        instance.date = validated_data.get('date', instance.date)
        instance.customer_name = validated_data.get(
            'customer_name', instance.customer_name
        )
        instance.save()
        # print(validated_data)
        for detail_data in details_data:
            detail_id = detail_data.get('id')
            print(detail_id)
            if detail_id:
                detail, created = InvoiceDetail.objects.update_or_create(
					id=detail_id, defaults=detail_data
				)
            else:
                detail = InvoiceDetail.objects.create(
                    invoice=instance, **detail_data
                )
            instance.details.add(detail)
        return instance
