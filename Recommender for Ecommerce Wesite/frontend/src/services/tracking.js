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

  async sendEvent(action, data = {}) {
    try {
      const payload = {
        session_id: this.sessionId,
        user_id: this.userId,
        action,
        timestamp: new Date().toISOString(),
        metadata: data
      };

      if (this.isOnline) {
        // Send to backend
        try {
          await ApiService.request('/activities/', {
            method: 'POST',
            body: JSON.stringify(payload),
            auth: !!this.userId
          });
          
          console.log('📊 Tracking Event Sent:', payload);
          return { success: true, data: payload };
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
      await this.sendBulkEvents(events);
    } catch (error) {
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
