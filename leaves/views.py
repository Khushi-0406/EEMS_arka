from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import LeaveRequest, LeaveBalance, LeaveType
from datetime import datetime



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def apply_leave(request):
    user = request.user

    leave_type_id = request.data.get('leave_type')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    reason = request.data.get('reason')

    # check leave type
    leave_type = LeaveType.objects.filter(id=leave_type_id).first()
    if not leave_type:
        return Response({"error": "Invalid leave type"})

    # convert dates
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    days = (end - start).days + 1

    # ❌ invalid date
    if days <= 0:
        return Response({"error": "Invalid date range"})

    # 🔥 overlap check (MUST BEFORE CREATE)
    existing = LeaveRequest.objects.filter(
        employee=user,
        start_date__lte=end_date,
        end_date__gte=start_date
    )

    if existing.exists():
        return Response({"error": "Leave dates overlap"})

    # check balance
    balance = LeaveBalance.objects.filter(
        employee=user,
        leave_type=leave_type
    ).first()

    if not balance:
        return Response({"error": "Leave balance not assigned"})

    if balance.remaining_days < days:
        return Response({"error": "Not enough leave balance"})

    # create request
    leave = LeaveRequest.objects.create(
        employee=user,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason
    )

    return Response({
        "message": "Leave applied successfully",
        "leave_id": leave.id,
        "days_requested": days
    })



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_leave(request, leave_id):
    user = request.user

    leave = LeaveRequest.objects.get(id=leave_id)
    action = request.data.get('action')

    # prevent re-approval
    if leave.status != "Pending":
        return Response({"error": "Already processed"})

    if action == "Approved":
        leave.status = "Approved"

        days = (leave.end_date - leave.start_date).days + 1

        balance = LeaveBalance.objects.get(
            employee=leave.employee,
            leave_type=leave.leave_type
        )

        # deduct balance
        balance.remaining_days -= days
        balance.save()

        leave.approved_by = user

    elif action == "Rejected":
        leave.status = "Rejected"
        leave.approved_by = user

    leave.save()

    return Response({
        "message": f"Leave {leave.status}"
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def leave_history(request):
    user = request.user

    leaves = LeaveRequest.objects.filter(employee=user)

    data = []
    for l in leaves:
        data.append({
            "id": l.id,
            "leave_type": l.leave_type.name,
            "start_date": l.start_date,
            "end_date": l.end_date,
            "status": l.status
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_leave_requests(request):

    leaves = LeaveRequest.objects.all()

    data = []
    for l in leaves:
        data.append({
            "employee": l.employee.username,
            "leave_type": l.leave_type.name,
            "start_date": l.start_date,
            "end_date": l.end_date,
            "status": l.status
        })

    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_leave_balance(request):
    user = request.user

    balances = LeaveBalance.objects.filter(employee=user)

    data = []
    for b in balances:
        data.append({
            "leave_type": b.leave_type.name,
            "remaining_days": b.remaining_days
        })

    return Response(data)