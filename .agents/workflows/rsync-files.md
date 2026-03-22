# Rsync Files Workflow

Steps to trigger and verify rsync between VM-2 and VM-3:

1. Ensure all services are running:
   ```bash
   docker compose up -d
   ```

2. Access the VM-2 backend container:
   ```bash
   docker compose exec vm2-backend bash
   ```

3. Inside the VM-2 container, you can manually trigger rsync:
   ```bash
   # Test rsync connection to VM-3
   rsync -avz --progress app_user@vm3-storage::company_data /tmp/test_sync/
   
   # Or use the Python service
   python -c "
   from app.services.rsync_service import RsyncService
   service = RsyncService()
   result = service.sync_from_storage()
   print('Sync result:', result)
   "
   ```

4. Verify files were synced:
   ```bash
   ls -la /tmp/test_sync/
   # You should see company data files that were seeded in VM-3
   ```

5. Check rsync daemon logs on VM-3:
   ```bash
   # In another terminal
   docker compose logs -f vm3-storage
   ```

6. To test the rsync service from your application:
   ```bash
   # From your local machine, you can test the service
   curl -X POST http://localhost:8000/admin/sync-files  # (if endpoint exists)
   ```

Note: The rsync service is designed to run automatically in the background as part of the VM-3 container's startup process. The VM-3 container runs both MySQL and the rsync daemon.

For development purposes, you can also manually populate the /rsync_data directory in VM-3 with test files that your Gemini service can search over.