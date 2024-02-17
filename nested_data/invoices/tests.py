from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_invoice_with_details(self):
        data = {
            "date": "2024-02-17",
            "customer_name": "Test Customer",
            "details": [
                {"description": "Test Description 1", "quantity": 1, "unit_price": 10, "price": 10},
                {"description": "Test Description 2", "quantity": 2, "unit_price": 20, "price": 40}
            ]
        }
        response = self.client.post("/api/invoices/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(InvoiceDetail.objects.count(), 2)

    def test_update_invoice_with_details(self):
        invoice = Invoice.objects.create(date="2024-02-17", customer_name="Test Customer 2")
        detail1 = InvoiceDetail.objects.create(invoice=invoice, description="Test Description 1", quantity=1, unit_price=10, price=10)
        detail2 = InvoiceDetail.objects.create(invoice=invoice, description="Test Description 2", quantity=2, unit_price=20, price=40)
        
        print("new invoice:", invoice, detail1, detail2)

        data = {
            "date": "2024-02-18",
            "customer_name": "Updated Customer",
            "details": [
                {"id": detail1.id, "description": "Updated Description 1", "quantity": 3, "unit_price": 30, "price": 90},
                {"id": detail2.id, "description": "Updated Description 2", "quantity": 4, "unit_price": 40, "price": 160}
            ]
        }
        response = self.client.put(f"/api/invoices/{invoice.id}/", data, format="json")
        
        print("updated: ", InvoiceDetail.objects.get(id=detail1.id), InvoiceDetail.objects.get(id=detail2.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(Invoice.objects.get(id=invoice.id).date), "2024-02-18")
        self.assertEqual(Invoice.objects.get(id=invoice.id).customer_name, "Updated Customer")
        self.assertEqual(InvoiceDetail.objects.get(id=detail1.id).description, "Updated Description 1")
        self.assertEqual(InvoiceDetail.objects.get(id=detail1.id).quantity, 3)
        self.assertEqual(InvoiceDetail.objects.get(id=detail1.id).price, 90)
        self.assertEqual(InvoiceDetail.objects.get(id=detail2.id).description, "Updated Description 2")
        self.assertEqual(InvoiceDetail.objects.get(id=detail2.id).quantity, 4)
        self.assertEqual(InvoiceDetail.objects.get(id=detail2.id).price, 160)

    def test_delete_invoice(self):
        invoice = Invoice.objects.create(date="2024-02-17", customer_name="Test Customer")
        detail1 = InvoiceDetail.objects.create(invoice=invoice, description="Test Description 1", quantity=1, unit_price=10, price=10)
        detail2 = InvoiceDetail.objects.create(invoice=invoice, description="Test Description 2", quantity=2, unit_price=20, price=40)

        response = self.client.delete(f"/api/invoices/{invoice.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(InvoiceDetail.objects.count(), 0)
