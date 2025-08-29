# 💳 E-commerce Payment Demo

Demo application showcasing payment processing sandbox with comprehensive frontend integration.

## 🚀 Quick Start

### Backend (Django + DRF)
```bash
cd backend
python manage.py runserver
```
Backend runs at: http://localhost:8000

### Frontend (React)
```bash
cd frontend
npm install
npm start
```
Frontend runs at: http://localhost:3000

## 🎯 Features Demonstrated

### 🔧 Payment Sandbox System
- ✅ Success payment scenarios (Visa, Mastercard)
- ❌ Decline scenarios (insufficient funds, expired card, etc.)
- 🔄 Webhook simulation and processing
- 💰 Refund capabilities (full/partial)
- 🔐 Security validation (HMAC signatures)
- 🌍 Multi-currency support
- 📊 Real-time payment status tracking

### 🖥️ Frontend Components

1. **🏠 Home Page** (`/`)
   - Landing page with feature overview
   - Quick navigation to all demos

2. **💳 Payment Processing** (`/payment`)
   - Interactive payment form
   - Test card number shortcuts
   - Real-time payment processing
   - Success/decline result display
   - Payment status checking

3. **🔧 Sandbox Info** (`/sandbox`)
   - Complete test card reference
   - API endpoint documentation
   - Webhook event simulator
   - Environment information

4. **🧪 API Integration Test** (`/test`)
   - Comprehensive API testing suite
   - End-to-end payment flow testing
   - Error handling demonstration
   - Real-time test results

## 🧪 Test Card Numbers

### ✅ Success Cards
- **Visa**: `4111111111111111`
- **Mastercard**: `5555555555554444`

### ❌ Decline Cards
- **Generic Decline**: `4000000000000002`
- **Insufficient Funds**: `4000000000000341`
- **Expired Card**: `4000000000000069`
- **Incorrect CVC**: `4000000000000127`
- **Lost Card**: `4000000000009987`
- **Stolen Card**: `4000000000009979`

## 🌐 API Endpoints

### Payment Processing
```
POST /api/v1/payments/charge/
GET  /api/v1/payments/{id}/status/
POST /api/v1/payments/{id}/refund/
```

### Sandbox Tools
```
GET  /api/v1/payments/sandbox/info/
POST /api/v1/payments/sandbox/webhook/{id}/
```

### Orders Management
```
POST /api/v1/orders/
GET  /api/v1/orders/{id}/
```

## 🔄 Payment Flow

1. **Create Order**
   - Customer info + items
   - Total amount calculation
   - Order status: `pending`

2. **Process Payment**
   - Payment method selection
   - Card validation
   - Sandbox processing
   - Status: `completed` or `declined`

3. **Webhook Handling**
   - Signature validation
   - Event processing
   - Status updates
   - Idempotency protection

4. **Status Tracking**
   - Real-time status checks
   - Payment confirmation
   - Error handling

## 🧩 Architecture

```
Frontend (React)     Backend (Django)     Sandbox System
     |                      |                    |
📱 Payment UI  ←→  🔌 REST APIs  ←→  💳 Payment Engine
📊 Status View ←→  📡 Webhooks   ←→  🔄 Event Simulator
🧪 API Tester  ←→  🛡️ Security   ←→  🔐 HMAC Validation
```

## 🎨 Usage Examples

### Make a Payment
1. Go to `/payment`
2. Select test card (click shortcuts)
3. Fill payment details
4. Click "Process Payment"
5. View results instantly

### Test Decline Scenarios
1. Use decline test cards
2. See different error messages
3. Verify proper error handling

### Simulate Webhooks
1. Go to `/sandbox`
2. Enter payment ID
3. Click webhook event buttons
4. See real-time processing

### Run API Tests
1. Go to `/test`
2. Click "Run API Tests"
3. Watch comprehensive integration testing
4. Review detailed results

## 🔒 Security Features

- ✅ HMAC SHA256 webhook signatures
- ✅ Timestamp validation (5-minute window)
- ✅ Replay attack protection
- ✅ Request idempotency
- ✅ Input sanitization
- ✅ Error handling

## 💡 Development Notes

- **Sandbox Mode**: All payments are simulated
- **No Real Money**: Safe for testing/development
- **CORS Enabled**: Frontend-backend communication
- **Hot Reload**: Changes reflect instantly
- **Comprehensive Logging**: Full request/response tracking

## 🚨 Important Notes

⚠️ **This is a DEMO system**
- Not for production use
- No real payment processing
- Test data only
- Development environment

✅ **Production Checklist** (when ready):
- [ ] Use real payment processor APIs
- [ ] Implement proper authentication
- [ ] Add rate limiting
- [ ] Set up monitoring
- [ ] Enable HTTPS
- [ ] Configure production database
- [ ] Add error tracking
- [ ] Implement audit logging

---

🎯 **Demo Objective**: Showcase complete payment system architecture with modern frontend integration and comprehensive testing capabilities.
