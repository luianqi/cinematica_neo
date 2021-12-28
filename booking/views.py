import decimal

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.models import *
from booking.serializers import (
    RoomSerializer,
    SeatSerializer,
    BookingSerializer,
    DiscountSerializer
)


class RoomList(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class SeatList(generics.ListCreateAPIView):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer


class DiscountList(generics.ListCreateAPIView):
    serializer_class = DiscountSerializer

    def get_queryset(self):
        return Discount.objects.filter(client=self.request.user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)


class BookingList(APIView):
    serializer_class = BookingSerializer

    def get(self, request):
        booking = Booking.objects.filter(client=request.user)
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():

            showtime = serializer.validated_data["showtime"]
            seat = serializer.validated_data["seat"]
            ticket_type = serializer.validated_data["ticket_type"]
            payment_method = serializer.validated_data["payment_method"]
            discount = serializer.validated_data["discount"]
            payment_value = serializer.validated_data["payment_value"]

            booking = Booking.objects.create(
                client=request.user,
                ticket_type=ticket_type,
                discount=discount,
                payment_method=payment_method,
                payment_value=payment_value,
                seat=seat,
                showtime=showtime,
            )

            if booking:
                discount = Discount.objects.get(client=self.request.user)
                discount.discount_card = discount.discount_card + (
                    decimal.Decimal(booking.ticket_type.price / 100 * 3)
                )
                discount.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )