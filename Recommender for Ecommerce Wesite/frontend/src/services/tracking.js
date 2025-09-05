import ApiService from './api';

class TrackingService {
  constructor() {
    this.sessionId = this.generateSessionId();
    this.userId = null;
    this.eventQueue = [];
    this.isOnline = navigator.onLine;
    
    // Listen for online/offline events
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.flushEventQueue();
    });
    
    window.addEventListener('offline', () => {
      this.isOnline = false;
    });
  }

  generateSessionId() {
    return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
  }

  setUser(userId) {
    this.userId = userId;
  }

  // Track product view activity
  async trackProductView(bookId) {
    return this.sendActivityEvent('view', bookId);
  }

  // Track product click activity  
  async trackProductClick(bookId) {
    return this.sendActivityEvent('view', bookId);  // Use 'view' instead of 'click'
  }

  // Track add to cart activity
  async trackAddToCart(bookId) {
    return this.sendActivityEvent('add_to_cart', bookId);
  }

  async sendActivityEvent(action, bookId, additionalData = {}) {
    try {
      const payload = {
        book_id: bookId,
        action: action,
        activity_time: new Date().toISOString(),
        ...additionalData
      };

      if (this.isOnline) {
        // Send to activity tracking API using ApiService.post
        const response = await ApiService.post('/activities/', payload);
        return response;
      } else {
        // Queue for later if offline
        this.eventQueue.push(payload);
        return { queued: true };
      }
    } catch (error) {
      console.error('Error tracking activity:', error);
      // Queue for retry if request fails
      this.eventQueue.push({
        book_id: bookId,
        action: action, 
        activity_time: new Date().toISOString(),
        ...additionalData
      });
      return { error: error.message };
    }
  }

  async sendEvent(action, data = {}) {
    try {
      // Map generic actions to activity API format
      const actionMapping = {
        'product_view': 'view',
        'add_to_cart': 'add_to_cart',
        'remove_from_cart': 'add_to_cart', // Map to existing action
        'page_view': 'view',
        'modal_open': 'view',
        'modal_close': 'view',
        'search': 'view'
      };

      const mappedAction = actionMapping[action] || 'view';
      const productId = data.product_id || data.book_id || 1; // fallback to default book

      const payload = {
        book_id: productId,
        action: mappedAction,
        activity_time: new Date().toISOString()
      };

      if (this.isOnline) {
        // Send to backend using activities API format
        try {
          const response = await ApiService.post('/activities/', payload);
          
          console.log('📊 Tracking Event Sent:', payload);
          return { success: true, data: response };
        } catch (error) {
          // If failed to send, add to queue
          this.eventQueue.push(payload);
          console.warn('📊 Tracking Event Queued:', payload);
          return { success: false, queued: true, error };
        }
      } else {
        // Offline, add to queue
        this.eventQueue.push(payload);
        console.log('📊 Tracking Event Queued (Offline):', payload);
        return { success: false, queued: true };
      }
    } catch (error) {
      console.error('❌ Tracking Error:', error);
      return { success: false, error };
    }
  }

  // Send bulk events
  async sendBulkEvents(events) {
    try {
      if (!this.isOnline) {
        this.eventQueue.push(...events);
        return { success: false, queued: true };
      }

      const response = await ApiService.request('/activities/bulk/', {
        method: 'POST',
        body: JSON.stringify({ events }),
        auth: !!this.userId
      });

      console.log('📊 Bulk Events Sent:', events.length, 'events');
      return { success: true, data: response };
    } catch (error) {
      // If failed, add to queue
      this.eventQueue.push(...events);
      console.error('❌ Bulk Tracking Error:', error);
      return { success: false, queued: true, error };
    }
  }

  // Flush queued events
  async flushEventQueue() {
    if (this.eventQueue.length === 0 || !this.isOnline) return;

    const events = [...this.eventQueue];
    this.eventQueue = [];

    try {
      // Try to send each queued activity event
      for (const event of events) {
        try {
          await ApiService.post('/activities/', event);
        } catch (error) {
          console.error('Failed to send queued activity:', error);
          // Put failed events back in queue
          this.eventQueue.push(event);
        }
      }
    } catch (error) {
      console.error('Error flushing event queue:', error);
      // If still failed, put back in queue
      this.eventQueue.unshift(...events);
    }
  }

  // Product tracking methods
  trackProductView(productId, productTitle) {
    return this.sendEvent('product_view', { 
      product_id: productId,
      product_title: productTitle
    });
  }

  trackAddToCart(productId, quantity = 1) {
    return this.sendEvent('add_to_cart', { 
      product_id: productId,
      quantity 
    });
  }

  trackRemoveFromCart(productId) {
    return this.sendEvent('remove_from_cart', { 
      product_id: productId 
    });
  }

  // Search tracking
  trackSearch(query, resultCount = 0) {
    return this.sendEvent('search', { 
      query,
      result_count: resultCount 
    });
  }

  // Page tracking
  trackPageView(page) {
    return this.sendEvent('page_view', { page });
  }

  // Modal tracking
  trackModalOpen(modalType, productId = null) {
    return this.sendEvent('modal_open', { 
      modal_type: modalType,
      product_id: productId 
    });
  }

  trackModalClose(modalType, duration = null) {
    return this.sendEvent('modal_close', { 
      modal_type: modalType,
      duration 
    });
  }
}

const trackingService = new TrackingService();
export default trackingService;
