from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .authentication import AdminAPISecretAuthentication 
from .models import Auction,Bid
from .serializers import AuctionSerializer, BidSerializer

class AuctionViewSet(viewsets.ModelViewSet):
    queryset = Auction.objects.all()
    serializer_class = AuctionSerializer
    authentication_classes = [AdminAPISecretAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def determine_winner(self):
        # Check if the auction has ended
        if self.end_time <= timezone.now():
            # Get all bids for this auction
            bids = Bid.objects.filter(auction=self)

            if bids:
                # Find the highest bid
                highest_bid = max(bids, key=lambda bid: bid.amount)

                # Update the winner and winning_bid fields
                self.winner = highest_bid.user
                self.save()




class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Get the auction_id from the request data
        auction_id = request.data.get('auction')

        try:
            # Check if the auction exists
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            return Response({'message': 'Auction does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the auction has not ended (you can add this logic based on the current time)

        # Associate the bid with the authenticated user
        request.data['user'] = request.user.pk

        serializer = BidSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
